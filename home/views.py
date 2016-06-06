from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from home.models import ChessUser, Challenge
from django import forms
from django.http import HttpResponseRedirect
from chess_logic.models import ChessGame
from django.views.decorators.csrf import csrf_exempt
import subprocess
import hashlib

class OpponentPicker(forms.Form):
    opponent = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(OpponentPicker, self).__init__(*args, **kwargs)
        choices = []
        for user in ChessUser.objects.all():
            choices.append((user.pk, user.username))
        self.fields['opponent'] = forms.ChoiceField(choices=choices)

@csrf_exempt
def beat(request):
    output = subprocess.check_output(["sudo", "git", "pull"])
    print output
    return HttpResponseRedirect("/")

def get_active_matches(request):
    """creates a list of active matches for player 1"""
    matches_player1 = []
    if request.session.get('player1', ''):
        p1 = request.session['player1']['pk']
        games = ChessGame.objects.filter(player_white_pk=p1) | ChessGame.objects.filter(player_black_pk=p1)
        for game in games:
            if game.game_over == "0":
                wp = ChessUser.objects.get(pk=game.player_white_pk).username
                bp = ChessUser.objects.get(pk=game.player_black_pk).username
                if str(game.player_white_pk) == str(p1) and game.turn == "hvit":
                    p1turn = True
                elif str(game.player_black_pk) == str(p1) and game.turn == "svart":
                    p1turn = True
                else:
                    p1turn = False

                if wp == "Magnus Carlsen" or bp == "Magnus Carlsen":
                    continue

                matches_player1.append((wp, bp, p1turn, game.pk))
    return matches_player1


def login_or_create_user(username, password):
    #check if user is in database
    try:
        user = ChessUser.objects.get(username=username)
        #check if correct password
        hex_password = hashlib.sha224(password).hexdigest()
        if not user.password == hex_password:
            user = None
    except:
        #do not create a user with empty username
        if len(username) > 1 and len(password) > 1:
            password = hashlib.sha224(password).hexdigest()
            user = ChessUser(username=username, password=password)
            user.save()

    return user

def index(request):
    if request.method == "POST":
        for post in request.POST:
            print post, request.POST[post]

        #logout player 1
        if 'logout_user_1' in request.POST:
            del request.session['player1']
            #if player2 make him player1
            if 'player2' in request.session:
                request.session['player1'] = request.session['player2']
                del request.session['player2']
            return HttpResponseRedirect(redirect_to="/")

        #logout player 2
        elif 'logout_user_2' in request.POST:
            del request.session['player2']
            return HttpResponseRedirect(redirect_to="/")

        #try to login user 1
        if 'login_user_1' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = login_or_create_user(username, password)

            if user: request.session['player1'] = {'username':user.username, 'pk':user.pk}
            return HttpResponseRedirect(redirect_to="/")

        #try to login user 2
        elif 'login_user_2' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = login_or_create_user(username, password)

            if user: request.session['player2'] = {'username':user.username, 'pk':user.pk}
            return HttpResponseRedirect(redirect_to="/")

        #challenge anoter user
        elif 'opponent' in request.POST:
            p1 = ChessUser.objects.get(pk=request.session['player1']['pk'])
            p2 = ChessUser.objects.get(pk=request.POST['opponent'])
            #Challenge Stockfish
            if p2.username == "Magnus Carlsen":
                request.session['player2'] = {'username':p2.username, 'pk':p2.pk}
                return redirect("/ai/?new_game=1")
            else:
                Challenge(player1=p1, player2=p2).save()
                return HttpResponseRedirect(redirect_to="/")

        #accept or deny challenge
        elif 'answer_challenge' in request.POST:
            if 'accept' in request.POST:
                return redirect('/game/?challenge=%s'%request.POST['accept'])
            elif 'deny' in request.POST:
                Challenge.objects.get(pk=request.POST['deny']).delete()
            return HttpResponseRedirect(redirect_to="/")


        #start a new game
        elif "start_game" in request.POST:
            return redirect("/game/?new_game=1")

        #continue a game
        elif "continue_game" in request.POST:
            return redirect("/game/?continue_game=%s"%request.POST["continue_game"])

    #gather all challenges for player1
    challenges_player1 = []
    if request.session.get('player1', ''):
        p1 = request.session['player1']
        challenges_player1 = Challenge.objects.filter(player2=p1['pk'])

    #gather all active matches for player1
    matches_player1 = get_active_matches(request)


    template = 'home/index.html'
    context = {'opponent_picker_form':OpponentPicker,
                'challenges_player1':challenges_player1,
                'matches_player1':matches_player1,}
    return render_to_response(template, context, context_instance=RequestContext(request))
