#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from chess_logic.models import ChessGame
import json
from chess_rules import init_bricks, move, checkmate, check, pawn_over, replace_pawn

def index(request):
    if "start_game" in request.POST:
        return redirect("/game/?new_game=1")
    template = 'index.html'
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))

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


def game(request):
    if 'new_game' in request.GET:
        #start a new game
        hb, sb = init_bricks()
        game_over = 0
        turn = "hvit"
        ab = {'hb':hb, 'sb':sb, 'game_over':game_over, "turn":turn}
        data = json.dumps(ab)
        board_html = generate_board()
        ChessGame(ab=data, turn="w", game_over="0").save()

    if 'replace' in request.GET:
        replace = request.GET['replace']
        allb = ChessGame.objects.last()
        ab = json.loads(allb.ab)
        hb = ab['hb']
        sb = ab['sb']
        print "here", allb.pawn_over
        if allb.pawn_over and (replace in ["D", "H", "T", "L"]):
            print "here"
            if allb.turn == "w":
                hb = replace_pawn(hb, replace)
                allb.turn = "b"
            else:
                sb = replace_pawn(sb, replace)
                allb.turn = "w"
            allb.pawn_over = False
        ab = {'hb':hb, 'sb':sb}
        allb.ab = json.dumps(ab)
        allb.save()




    if 'move' in request.GET:
        this_move = request.GET['move']
        allb = ChessGame.objects.last()

        ab = json.loads(allb.ab)
        hb = ab['hb']
        sb = ab['sb']
        gameover = int(allb.game_over)

        if allb.turn == "w":
            if gameover == 0:
                _hb, _sb = move(hb, sb, this_move[:2], this_move[2:], hb, sb)
                if hb != _hb:
                    ab = {'hb':_hb, 'sb':_sb}
                    allb.turn = "b"
                    if pawn_over(_hb):
                        print "pawn over"
                        allb.pawn_over = True
                        allb.turn = "w"

                if checkmate(_sb, _hb, _hb, _sb):
                    if check(_sb, _hb, _hb, _sb):
                        gameover = 1
                        allb.turn = "w"
                    else:
                        gameover = 2
                        allb.turn = "w"

        elif allb.turn == "b":
            if gameover == 0:
                _sb, _hb = move(sb, hb, this_move[:2], this_move[2:], hb, sb)
                if sb != _sb:
                    ab = {'hb':_hb, 'sb':_sb}
                    allb.turn = "w"
                    if pawn_over(_sb):
                        allb.pawn_over = True
                        allb.turn = "b"

                if checkmate(_hb, _sb, _hb, _sb):
                    if check(_hb, _sb, _hb, _sb):
                        gameover = 1
                        allb.turn = "b"
                    else:
                        gameover = 2
                        allb.turn = "b"
        
        if (allb.turn == 'w'):
            turn = 'hvit'
        else:
            turn = 'svart'

        allb.ab = json.dumps(ab)
        allb.game_over = str(gameover)
        allb.save()

        ab['game_over'] = gameover
        ab['turn'] = turn;
        ab['pawn_over'] = allb.pawn_over
        data = json.dumps(ab)

        return HttpResponse(data)

    if 'status' in request.GET:
        pass

    all_b = ChessGame.objects.last()
    template = 'game.html'
    context = {'bricks':all_b.ab,
                'board':generate_board(),
                'turn':str(all_b.turn),
                }

    return render_to_response(template, context, context_instance=RequestContext(request))
