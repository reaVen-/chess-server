#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from random import randint as random_int

from channels import Group
from home.models import Challenge, ChessUser

from chess_logic.models import ChessGame
import json, subprocess, time
from chess_rules import init_bricks, move, checkmate, check, pawn_over, replace_pawn
from home.views import get_active_matches
from chess_logic.tasks import make_ai_move

def generate_board():
    counter = 0
    board_html = ""
    for x in "12345678":
        for y in "ABCDEFGH":
            board_html += '<div id=\"%s%s\" class='%(y, x)
            if counter % 2 == 0:
                board_html += '\"grid white\"></div>'
            else:
                board_html += '\"grid black\"></div>'
            counter += 1
        counter += 1
        board_html += "<br>"
    return board_html

def do_move(request, ai_move=None):
    if ai_move:
        this_move = ai_move
    else:
        this_move = request.GET['move']
    cg = ChessGame.objects.get(pk=request.session['game_id'])

    ab = json.loads(cg.ab)
    hb = ab['hb']
    sb = ab['sb']
    gameover = cg.game_over

    start = this_move[:2]
    end = this_move[2:]

    castling_left = False
    castling_right = False

    allow_move_black = True
    allow_move_white = True

    #check if this user can move
    if not 'player2' in request.session:
        #figgure out if player1 is white or black
        if str(request.session['player1']['pk']) == str(cg.player_white_pk):
            allow_move_black = False
        else:
            allow_move_white = False


    if cg.turn == "hvit" and allow_move_white:
        #if game is not finished
        if gameover == "0":
            #figgure out if castling is allowed
            #check if user is trying to move king for first time
            if hb[start] == "Konge" and cg.white_king_moved == False:
                #check if user tries castling right
                if end == "F1" and cg.white_tower_right_moved == False:
                    #set castling to true
                    castling_right = True
                #check if user tries castling left
                elif end == "B1" and cg.white_tower_left_moved == False:
                    #set castling to true
                    castling_left = True

            #try to move
            _hb, _sb = move(hb, sb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
            #check if move was succesful
            if hb != _hb:
                #update bricks in database
                ab = {'hb':_hb, 'sb':_sb}
                #check if white moved his king or tower
                if start == "D1" and hb[start] == "Konge":
                    cg.white_king_moved = True

                #check if white moved his tower from initial position
                if start == "A1" and hb[start] == "Trn":
                    cg.white_tower_left_moved = True
                elif start == "H1" and hb[start] == "Trn":
                    cg.white_tower_right_moved = True

                #change turn
                cg.turn = "svart"
                if pawn_over(_hb):
                    cg.pawn_over = True
                    cg.turn = "hvit"

            if checkmate(_sb, _hb, _hb, _sb):
                if check(_sb, _hb, _hb, _sb):
                    gameover = "1"
                    cg.turn = "hvit"
                else:
                    gameover = "2"
                    cg.turn = "hvit"

    elif cg.turn == "svart" and allow_move_black:
        if gameover == "0":
            #figgure out if castling is allowed
            #check if user is trying to move king for first time
            if sb[start] == "Konge" and cg.black_king_moved == False:
                #check if user tries castling right
                if end == "F8" and cg.black_tower_right_moved == False:
                    #set castling to true
                    castling_right = True
                elif end == "B8" and cg.black_tower_left_moved == False:
                    #set castling to true
                    castling_left = True

            _sb, _hb = move(sb, hb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
            if sb != _sb:
                ab = {'hb':_hb, 'sb':_sb}
                #check if black moved his king from initial position
                if start == "D8" and sb[start] == "Konge":
                    cg.black_king_moved = True

                #check if black moved his tower from initial position
                if start == "A8" and sb[start] == "Trn":
                    cg.black_tower_left_moved = True
                elif start == "H8" and sb[start] == "Trn":
                    cg.black_tower_right_moved = True

                cg.turn = "hvit"
                if pawn_over(_sb):
                    cg.pawn_over = True
                    cg.turn = "svart"

            if checkmate(_hb, _sb, _hb, _sb):
                if check(_hb, _sb, _hb, _sb):
                    gameover = "1"
                    cg.turn = "svart"
                else:
                    gameover = "2"
                    cg.turn = "svart"
    
    cg.ab = json.dumps(ab)
    cg.game_over = gameover
    cg.save()

    ab['game_over'] = gameover
    ab['turn'] = cg.turn;
    ab['pawn_over'] = cg.pawn_over
    data = json.dumps(ab)

    Group("id-"+str(cg.pk)).send({'text':data})

    return HttpResponse(data)


def game(request):
    if not 'player1' in request.session:
        return HttpResponseRedirect(redirect_to="/")

    if 'challenge' in request.GET:
        ch = Challenge.objects.get(pk=request.GET['challenge'])
        p1 = request.session['player1']['pk']
        p2 = ch.player1.pk

        if random_int(1, 10) > 5:
            p1, p2 = p2, p1

        ab = init_bricks()
        data = json.dumps(ab)
        cg = ChessGame(ab=data, player_white_pk=p1, player_black_pk=p2)
        cg.save()
        request.session['game_id'] = cg.pk
        ch.delete()
        return HttpResponseRedirect(redirect_to="/game/")


    if 'new_game' in request.GET:
        #start a new game
        player1 = request.session.get("player1", "ANONYMOUS")
        player2 = request.session.get("player2", "ANONYMOUS")

        #player1 is white, swap then randomly before assigning
        if random_int(1, 10) > 5:
            player1, player2 = player2, player1

        ab = init_bricks()
        data = json.dumps(ab)
        cg = ChessGame(ab=data, player_white_pk=player1['pk'], player_black_pk=player2['pk'])
        cg.save()
        request.session['game_id'] = cg.pk
        return HttpResponseRedirect(redirect_to="/game/")

    if 'continue_game' in request.GET:
        #continue a game
        game = ChessGame.objects.get(pk=int(request.GET['continue_game']))
        request.session['game_id'] = game.pk
        return HttpResponseRedirect(redirect_to="/game/")


    if 'replace' in request.GET:
        replace = request.GET['replace']
        cg = ChessGame.objects.get(pk=request.session['game_id'])
        ab = json.loads(cg.ab)
        hb = ab['hb']
        sb = ab['sb']
        if cg.pawn_over and (replace in ["D", "H", "T", "L"]):
            if cg.turn == "hvit":
                hb = replace_pawn(hb, replace)
                cg.turn = "svart"
            else:
                sb = replace_pawn(sb, replace)
                cg.turn = "hvit"
            cg.pawn_over = False
        ab = {'hb':hb, 'sb':sb}
        cg.ab = json.dumps(ab)
        cg.save()
        return HttpResponseRedirect(redirect_to="/game/")

    if 'move' in request.GET:
        return do_move(request)

    all_b = ChessGame.objects.get(pk=request.session['game_id'])
    template = 'game.html'
    matches = get_active_matches(request)
    context = {'bricks':all_b.ab,
                'board':generate_board(),
                'turn':all_b.turn,
                'player_white':all_b.player_white_pk,
                'player_black':all_b.player_black_pk,
                'game_over':all_b.game_over,
                'player1':json.dumps(request.session['player1']),
                'player1pk':request.session['player1']['pk'],
                'player1name':request.session['player1']['username'],
                'matches':matches,
                'game_id':request.session['game_id']
                }

    if 'player2' in request.session:
        context['player2'] = json.dumps(request.session['player2'])
        context['player2pk'] = request.session['player2']['pk']
        context['player2name'] = request.session['player2']['username']
    else:
        if str(request.session['player1']['pk']) == str(all_b.player_white_pk):
            context['player2pk'] = all_b.player_black_pk
            context['player2name'] = ChessUser.objects.get(pk=context['player2pk']).username
        else:
            context['player2pk'] = all_b.player_white_pk
            context['player2name'] = ChessUser.objects.get(pk=context['player2pk']).username
    

    return render_to_response(template, context, context_instance=RequestContext(request))

def ai(request):
    if not 'player1' in request.session:
        print "player 1 missing - redirecting to /"
        return HttpResponseRedirect(redirect_to="/")
    if not 'player2' in request.session:
        request.session['player2'] = ChessUser.objects.get(username="Magnus Carlsen")

    if request.method == "GET" and 'new_game' in request.GET:
        player1 = request.session.get("player1", "ANONYMOUS")
        player2 = request.session.get("player2", "ANONYMOUS")

        #player1 is white, swap then randomly before assigning
        if random_int(1, 10) > 5:
            player1, player2 = player2, player1

        ab = init_bricks()
        data = json.dumps(ab)
        cg = ChessGame(ab=data, player_white_pk=player1['pk'], player_black_pk=player2['pk'])
        cg.save()
        request.session['game_id'] = cg.pk
        return HttpResponseRedirect("/ai/")

    if not 'game_id' in request.session:
        return HttpResponseRedirect("/ai/?new_game=1")

    #get game object
    cg = ChessGame.objects.get(pk=int(request.session['game_id']))

    #make ai move (will only move if its his turn)
    make_ai_move.delay(int(cg.pk))

    if request.method == "GET" and 'move' in request.GET:
        response = do_move(request)
        make_ai_move.delay(int(cg.pk))
        return response

    context = {'bricks':cg.ab,
                'board':generate_board(),
                'turn':cg.turn,
                'player_white':cg.player_white_pk,
                'player_black':cg.player_black_pk,
                'game_over':cg.game_over,
                'player1':json.dumps(request.session['player1']),
                'player1pk':request.session['player1']['pk'],
                'player1name':request.session['player1']['username'],
                'player2':json.dumps(request.session['player2']),
                'player2pk':request.session['player2']['pk'],
                'player2name':request.session['player2']['username'],
                'game_id':request.session['game_id']
                }

    return render_to_response("game.html", context, context_instance=RequestContext(request))

