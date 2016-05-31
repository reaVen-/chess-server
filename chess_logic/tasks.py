from __future__ import absolute_import

from celery import shared_task

from chess_logic.models import ChessGame

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def make_ai_move(game_id):
	game_data = ChessGame.objects.get(pk=game_id)
	game_data.ab = json.loads(game_data.ab)
    fen = generate_fen(game_data.__dict__)
    best_move = get_best_move(fen).upper()
	return 'FINISHED TASK - BEST MOVE: %s' % best_move


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
    get(engine)

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

