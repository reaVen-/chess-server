#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from chess_logic.models import ChessGame
import json
from chess_rules import init_bricks, move, checkmate, check, pawn_over, replace_pawn

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

        start = this_move[:2]
        end = this_move[2:]

        castling_left = False
        castling_right = False

        if allb.turn == "w":
            #if game is not finished
            if gameover == 0:
                #figgure out if castling is allowed
                #check if user is trying to move king for first time
                if hb[start] == "Konge" and allb.white_king_moved == False:
                    #check if user tries castling right
                    if end == "G1" and allb.white_tower_right_moved == False:
                        #set castling to true
                        castling_right = True
                    #check if user tries castling left
                    elif end == "C1" and allb.white_tower_left_moved == False:
                        #set castling to true
                        castling_left = True

                #try to move
                _hb, _sb = move(hb, sb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
                #check if move was succesful
                if hb != _hb:
                    #update bricks in database
                    ab = {'hb':_hb, 'sb':_sb}
                    #check if white moved his king or tower
                    if start == "E1" and hb[start] == "Konge":
                        allb.white_king_moved = True

                    #check if white moved his tower from initial position
                    if start == "A1" and hb[start] == "Trn":
                        allb.white_tower_left_moved = True
                    elif start == "H1" and hb[start] == "Trn":
                        allb.white_tower_right_moved = True

                    #change turn
                    allb.turn = "b"
                    if pawn_over(_hb):
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
                #figgure out if castling is allowed
                #check if user is trying to move king for first time
                if sb[start] == "Konge" and allb.black_king_moved == False:
                    #check if user tries castling right
                    if end == "G8" and allb.black_tower_right_moved == False:
                        #set castling to true
                        castling_right = True
                    elif end == "C8" and allb.black_tower_left_moved == False:
                        #set castling to true
                        castling_left = True

                _sb, _hb = move(sb, hb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
                if sb != _sb:
                    ab = {'hb':_hb, 'sb':_sb}
                    #check if black moved his king from initial position
                    if start == "E8" and sb[start] == "Konge":
                        allb.black_king_moved = True

                    #check if black moved his tower from initial position
                    if start == "A8" and sb[start] == "Trn":
                        allb.black_tower_left_moved = True
                    elif start == "H8" and sb[start] == "Trn":
                        allb.black_tower_right_moved = True

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