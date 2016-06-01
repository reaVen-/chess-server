from __future__ import absolute_import
from celery import shared_task
from chess_logic.models import ChessGame
from home.models import ChessUser
from .chess_rules import move, checkmate, check, pawn_over, replace_pawn, brick_to_index

import json, subprocess, time

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def make_ai_move(game_id):
    game_data = ChessGame.objects.get(pk=game_id)
    if ai_turn(game_data) and not game_data.looking_for_move:
        game_data.looking_for_move = True
        game_data.save()
        game_data.ab = json.loads(game_data.ab)
        fen = generate_fen(game_data.__dict__)
        best_move = get_best_move(fen).upper()
        do_move(best_move, game_data)
        game_data.looking_for_move = False
        return 'FINISHED TASK - BEST MOVE: %s' % best_move
    else:
        return 'FINISHED TASK - NOT MY TURN'

def ai_turn(cg):
    ai = ChessUser.objects.get(username="Magnus Carlsen")
    if cg.turn == "hvit":
        if str(ai.pk) == str(cg.player_white_pk):
            return True
    else:
        if str(ai.pk) == str(cg.player_black_pk):
            return True
    return False


def do_move(this_move, cg):
    ab = cg.ab
    hb = ab['hb']
    sb = ab['sb']
    gameover = cg.game_over

    start = this_move[:2]
    end = this_move[2:]



    if cg.turn == "hvit":
        #if game is not finished
        if gameover == "0":
            #figgure out if castling is allowed
            castling_left, castling_right = False, False
            if not cg.white_king_moved and not cg.white_tower_left_moved:
                castling_left = True
            if not cg.white_king_moved and not cg.white_tower_right_moved:
                castling_left = True

            #try to move
            _hb, _sb = move(hb, sb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
            #check if move was succesful
            if hb != _hb:
                #update bricks in database
                ab = {'hb':_hb, 'sb':_sb}
                #check if white moved his king or tower
                if start == "E1" and hb[start] == "Konge":
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

    elif cg.turn == "svart":
        if gameover == "0":
            #figgure out if castling is allowed
            castling_left, castling_right = False, False
            if not cg.black_king_moved and not cg.black_tower_left_moved:
                castling_left = True
            if not cg.black_king_moved and not cg.black_tower_right_moved:
                castling_left = True

            _sb, _hb = move(sb, hb, start, end, hb, sb, castling_left=castling_left, castling_right=castling_right)
            if sb != _sb:
                ab = {'hb':_hb, 'sb':_sb}
                #check if black moved his king from initial position
                if start == "E8" and sb[start] == "Konge":
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


def put(command, engine):
    engine.stdin.write(command+'\n')

def get(engine):
    engine.stdin.write('isready\n')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            return text
        if text.startswith("bestmove"):
            return text

def get_best_move(fen):
    engine = subprocess.Popen('/usr/games/stockfish', universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    get(engine)
    put("position fen %s"%fen, engine)
    get(engine)
    put("go movetime 5000", engine)
    time.sleep(6)
    try:
        best_move = get(engine).split(" ")[1]
    except:
        best_move = "Could not find a best move.. Sorry :("

    put("quit",engine)

    return best_move

def generate_fen(game_data):
    pieces = ["11111111", "11111111", "11111111", "11111111", "11111111", "11111111", "11111111", "11111111"]
    new_pieces = []
    hb = game_data['ab']['hb']
    sb = game_data['ab']['sb']
    turn = "w" if game_data['turn'] == "hvit" else "b"
    castling = ""

    #figgure out who can castle and where
    if not game_data['white_king_moved'] and not game_data['white_tower_right_moved']:
        castling += "K"
    if not game_data['white_king_moved'] and not game_data['white_tower_left_moved']:
        castling += "Q"
    if not game_data['black_king_moved'] and not game_data['black_tower_right_moved']:
        castling += "k"
    if not game_data['black_king_moved'] and not game_data['black_tower_left_moved']:
        castling += "q"

    castling = castling if castling != "" else "-"

    for b in sb:
        x, y = brick_to_index(b)
        pieces[x] = pieces[x][:y] + trans(sb[b]) + pieces[x][y+1:]

    for b in hb:
        x, y = brick_to_index(b)
        pieces[x] = pieces[x][:y] + trans(hb[b]).upper() + pieces[x][y+1:]

    for rank in pieces:
        s, cur = "", 0
        for pos in rank:
            if pos == "1":
                cur += 1
            else:
                s = s + str(cur) + pos if cur > 0 else s + pos
                cur = 0
        s = s + str(cur) if cur > 0 else s
        new_pieces.append(s)

    return "/".join(new_pieces) + " " + turn + " " + castling + " - " + "0 0"

def trans(s):
    d = {'Trn':'r', 'Lper':'b', 'Hest':'n', 'Dronning':'q', 'Konge':'k', 'Bonde':'p'}
    return d[s]

