#-*- coding: utf-8 -*-
def init_bricks():
    hb = {"A1":"Trn", "B1":"Hest", "C1":"Lper","D1":"Dronning","E1":"Konge","F1":"Lper","G1":"Hest","H1":"Trn",
          "A2":"Bonde", "B2":"Bonde", "C2":"Bonde", "D2":"Bonde", "E2":"Bonde", "F2":"Bonde", "G2":"Bonde", "H2":"Bonde"}
    sb = {"A8":"Trn", "B8":"Hest", "C8":"Lper","D8":"Dronning","E8":"Konge","F8":"Lper","G8":"Hest","H8":"Trn",
          "A7":"Bonde", "B7":"Bonde", "C7":"Bonde", "D7":"Bonde", "E7":"Bonde", "F7":"Bonde", "G7":"Bonde", "H7":"Bonde"}
    return hb, sb

def brick_to_index(brick):
    return (int(brick[1])-((int(brick[1])-4)*2), ord(brick[0])-65)

def index_to_brick(index):   
    return chr(index[1]+65)+str(8-index[0])

def get_straight(brick):
    x_pos, y_pos = brick_to_index(brick)
    upper = [(x, y_pos) for x in range(x_pos,-1,-1) if x < x_pos]
    lower = [(x, y_pos) for x in range(x_pos,8) if x > x_pos]
    left =  [(x_pos, y) for y in range(y_pos, -1, -1) if y < y_pos]
    right = [(x_pos, y) for y in range(y_pos, 8) if y > y_pos]
    return [upper, lower, left, right]

def get_adjacent(brick):
    x_pos, y_pos = brick_to_index(brick)
    upper_r = [(x_pos+c, y_pos-c) for c in range(-1, y_pos-8, -1) if 0 <= x_pos+c <= 7 and 0 <= y_pos-c <= 7]
    upper_l = [(x_pos-c, y_pos-c) for c in range(1, 8) if 0 <= y_pos-c <= 7 and 0 <= x_pos-c <= 7]
    lower_r = [(x_pos+c, y_pos+c) for c in range(1, 8) if 0 <= x_pos+c <= 7 and 0 <= y_pos+c <= 7]
    lower_l = [(x_pos+c, y_pos-c) for c in range(1, 8) if 0 <= x_pos+c <= 7 and 0 <= y_pos-c <= 7]
    return [upper_r, upper_l, lower_r, lower_l]

def legal_moves(brick, pb, ob, hb, sb):
    """returns a list of legal moves from brick"""
    kind = pb.get(brick, "z")[0]
    index = brick_to_index(brick)
    legal_moves = []
    if kind == "L":
        moves = get_adjacent(brick)
    elif kind == "D":
        moves = get_adjacent(brick)+get_straight(brick)
    elif kind == "T":
        moves = get_straight(brick)
    elif kind == "H":
        delta = [(-2, 1), (-2,-1), (2, 1), (2,-1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        moves =[[(x+index[0], y+index[1])] for x,y in delta if 0 <= x+index[0] <= 7 and 0 <= y+index[1] <= 7]
    elif kind == "K":
        #should also make it possible to do a 'rokade'
        delta = [(-1, 0),(1, 0),(1, 1),(0, 1),(-1, 1),(1, -1),(0, -1),(-1,-1)]
        moves =[[(x+index[0], y+index[1])] for x,y in delta if 0 <= x+index[0] <= 7 and 0 <= y+index[1] <= 7]
    elif kind == "B":
        #denne koden er alt for stygg
        moves = []
        if brick in hb:
            attack = [(-1+index[0], -1+index[1]), (-1+index[0], 1+index[1])]
            move =   [(-1+index[0], index[1]), (-2+index[0], index[1])]
            if brick[1] != "2": del move[-1]
        else: 
            attack = [(1+index[0], -1+index[1]), (1+index[0], 1+index[1])]
            move = [(1+index[0], index[1]), (2+index[0], index[1])]
            if brick[1] != "7": del move[-1]
        for x in attack:
            this_brick = index_to_brick(x)
            if this_brick in ob:
                legal_moves.append(this_brick)
        for x in move:
            this_brick = index_to_brick(x)
            if this_brick in pb or this_brick in ob:
                break
            else:
                legal_moves.append(this_brick)

        return legal_moves
    else:
        return []

    for direction in moves:
        for move in direction:
            this_brick = index_to_brick(move)
            if this_brick in pb:
                break
            else:
                if this_brick in ob:
                    legal_moves.append(this_brick)
                    break
                legal_moves.append(this_brick)

    return legal_moves

def make_new(start, end, hb, sb):
    """moves one piece and updates the dictionary"""
    if start in hb:
        pb = hb.copy()
        ob = sb.copy()
    elif start in sb:
        pb = sb.copy()
        ob = hb.copy()

    pb[end] = pb[start]
    del pb[start]
    try: del ob[end]
    except: pass
    return pb, ob

def check(pb, ob, hb, sb):
    """function to test if pb is in check"""
    king = [x[0] for x in pb.items() if x[1]=="Konge"][0]
    for key in ob.keys():
        moves = legal_moves(key, ob, pb, hb, sb)
        for move in moves:
            if move == king:
                return True
    return False

def checkmate(pb, ob, hb, sb):
    """function to test if pb is in checkmate"""
    for key in pb.keys():
        moves = legal_moves(key, pb, ob, hb, sb)
        for move in moves:
            _pb, _ob = make_new(key, move, hb, sb)
            if not check(_pb, _ob, hb, sb):
                return False
    return True

def pawn(choice):
    d = {'D':'Dronning', 'T':'Trn', 'L':'Lper', 'H':'Hest'}
    return d[choice]

def move(pb, ob, start, end, hb, sb):
    """fix this function """
    if start not in pb:
        return pb, ob
    if end not in legal_moves(start, pb, ob, hb, sb):
        return pb, ob

    _pb, _ob = make_new(start, end, hb, sb)
    if not check(_pb, _ob, hb, sb): #mistake here
        pb, ob = make_new(start, end, hb, sb)
        if end[1] == ("1" or "8") and pb[end][0] == "B":
            print("Du har muilighet til å forfremme bonden")
            print("D = Dronning\nT = Tårn\nL = Løper\nH = Hest\nB = Bonde")
            choice = ""
            while choice not in ["D", "T", "L", "H"]:
                choice = raw_input("Velg en:")
            pb[end] = pawn(choice)
    return pb, ob