#-*- coding: utf-8 -*-
def init_bricks():
    hb = {"A1":"Trn", "B1":"Hest", "C1":"Lper","D1":"Konge","E1":"Dronning","F1":"Lper","G1":"Hest","H1":"Trn",
          "A2":"Bonde", "B2":"Bonde", "C2":"Bonde", "D2":"Bonde", "E2":"Bonde", "F2":"Bonde", "G2":"Bonde", "H2":"Bonde"}
    sb = {"A8":"Trn", "B8":"Hest", "C8":"Lper","D8":"Konge","E8":"Dronning","F8":"Lper","G8":"Hest","H8":"Trn",
          "A7":"Bonde", "B7":"Bonde", "C7":"Bonde", "D7":"Bonde", "E7":"Bonde", "F7":"Bonde", "G7":"Bonde", "H7":"Bonde"}
    return {'hb':hb, 'sb':sb}


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

def legal_moves(brick, pb, ob, hb, sb, castling_left=False, castling_right=False):
    """returns a list of legal moves from brick"""
    kind = pb.get(brick, "z")[0]
    index = brick_to_index(brick)
    legal_moves_list = []
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
        #should also make it possible to do castling
        #castle code
        if castling_left or castling_right:
            #check if its white turn
            if hb == pb:
                #check if left tower is there
                if hb.get("A1", "") == "Trn" and castling_left:
                    #check if path is clear for castling
                    a = hb.get("B1", "") + hb.get("C1", "")
                    b = sb.get("B1", "") + sb.get("C1", "")
                    if a + b == "":
                        #check if king can move without getting in chess
                        _hb, _sb = make_new("D1", "C1", hb, sb)
                        if not check(_hb, _sb, _hb, _sb):
                            _hb, _sb = make_new("C1", "B1", _hb, _sb)
                            if not check(_hb, _sb, _hb, _sb):
                                legal_moves_list.append("B1")
                #check if right tower is there
                if hb.get("H1", "") == "Trn" and castling_right:
                    #check if path is clear for castling
                    a = hb.get("G1", "") + hb.get("F1", "") + hb.get("E1", "")
                    b = sb.get("G1", "") + sb.get("F1", "") + hb.get("E1", "")
                    if a + b == "":
                        #check if king can move without getting in chess
                        _hb, _sb = make_new("D1", "E1", hb, sb)
                        if not check(_hb, _sb, _hb, _sb):
                            _hb, _sb = make_new("E1", "F1", _hb, _sb)
                            if not check(_hb, _sb, _hb, _sb):
                                _hb, _sb = make_new("F1", "G1", _hb, _sb)
                                if not check(_hb, _sb, _hb, _sb):
                                    legal_moves_list.append("G1")
            elif sb == pb:
                #check if left tower is there
                if sb.get("A8", "") == "Trn" and castling_left:
                    #check if path is clear for castling
                    a = hb.get("B8", "") + hb.get("C8", "")
                    b = sb.get("B8", "") + sb.get("C8", "")
                    if a + b == "":
                        #check if king can move without getting in chess
                        _sb, _hb = make_new("D8", "C8", hb, sb)
                        if not check(_sb, _hb, _hb, _sb):
                            _sb, _hb = make_new("C8", "B8", _hb, _sb)
                            if not check(_sb, _hb, _hb, _sb):
                                legal_moves_list.append("B8")
                #check if right tower is there
                if sb.get("H8", "") == "Trn" and castling_right:
                    #check if path is clear for castling
                    a = hb.get("G8", "") + hb.get("F8", "") + hb.get("E8", "")
                    b = sb.get("G8", "") + sb.get("F8", "") + sb.get("E8", "")
                    if a + b == "":
                        #check if king can move without getting in chess
                        _sb, _hb = make_new("D8", "E8", hb, sb)
                        if not check(_sb, _hb, _hb, _sb):
                            _sb, _hb = make_new("E8", "F8", _hb, _sb)
                            if not check(_sb, _hb, _hb, _sb):
                                _sb, _hb = make_new("F8", "G8", _hb, _sb)
                                    if not check(_sb, _hb, _hb, _sb):
                                        legal_moves_list.append("G8")

        #castle code
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
                legal_moves_list.append(this_brick)
        for x in move:
            this_brick = index_to_brick(x)
            if this_brick in pb or this_brick in ob:
                break
            else:
                legal_moves_list.append(this_brick)

        return legal_moves_list
    else:
        return []

    for direction in moves:
        for move in direction:
            this_brick = index_to_brick(move)
            if this_brick in pb:
                break
            else:
                if this_brick in ob:
                    legal_moves_list.append(this_brick)
                    break
                legal_moves_list.append(this_brick)

    return legal_moves_list

def make_new(start, end, hb, sb):
    """moves one piece and updates the dictionary"""
    if start in hb:
        pb = hb.copy()
        ob = sb.copy()
    elif start in sb:
        pb = sb.copy()
        ob = hb.copy()

    #move tower if user is castling
    if (start == "D8" or start == "D1") and pb[start] == "Konge":
        if end == "F8":
            pb["E8"] = "Trn"
            del pb["H8"]
        elif end == "B8":
            pb["C8"] = "Trn"
            del pb["A8"]
        elif end == "F1":
            pb["E1"] = "Trn"
            del pb["H1"]
        elif end == "B1":
            pb["C1"] = "Trn"
            del pb["A1"]

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

def move(pb, ob, start, end, hb, sb, castling_left=False, castling_right=False):
    """fix this function """
    if start not in pb:
        return pb, ob
    if end not in legal_moves(start, pb, ob, hb, sb, castling_left=castling_left, castling_right=castling_right):
        return pb, ob

    _pb, _ob = make_new(start, end, hb, sb)
    if not check(_pb, _ob, hb, sb): #mistake here
        pb, ob = _pb, _ob

    return pb, ob

def pawn_over(pb):
    """check if pawn is over"""
    for pos in pb.keys():
        if pos[1] in "18" and pb[pos] == "Bonde":
            return True
    return False

def replace_pawn(pb, choice):
    """replace the pawn that has crossed over to the other side"""
    for pos in pb.keys():
        if pos[1] in "18" and pb[pos] == "Bonde":
            pb[pos] = pawn(choice)
    return pb