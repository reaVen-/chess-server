from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from home.models import ChessUser, Challenge
from django import forms
from chess_logic.models import ChessGame

import hashlib

class OpponentPicker(forms.Form):
    opponent = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(OpponentPicker, self).__init__(*args, **kwargs)
        choices = []
        for user in ChessUser.objects.all():
            choices.append((user.pk, user.username))
        self.fields['opponent'] = forms.ChoiceField(choices=choices)


def login_or_create_user(username, password):
    #check if user is in database
    try:
        user = ChessUser.objects.get(username=username)
        print user
        #check if correct password
        if not user.password == password:
            user = None
    except:
        user = ChessUser(username=username, password=password)
        user.save()

    return user

def index(request):
    if request.method == "POST":
        #logout player 1
        if 'logout_user_1' in request.POST:
            del request.session['player1']
            #if player2 make him player1
            if 'player2' in request.session:
                request.session['player1'] = request.session['player2']
                del request.session['player2']
        #logout player 2
        elif 'logout_user_2' in request.POST:
            del request.session['player2']

        #try to login user 1
        if 'login_user_1' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            password = hashlib.sha224(password).hexdigest()
            user = login_or_create_user(username, password)

            if user: request.session['player1'] = {'username':user.username, 'pk':user.pk}

        #try to login user 2
        elif 'login_user_2' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            password = hashlib.sha224(password).hexdigest()
            user = login_or_create_user(username, password)

            if user: request.session['player2'] = {'username':user.username, 'pk':user.pk}

        #challenge anoter user
        elif 'opponents' in request.POST:
            p1 = ChessUser.objects.get(pk=request.session['player1']['pk'])
            p2 = ChessUser.objects.get(pk=request.POST['opponents'])
            Challenge(player1=p1, player2=p2).save()

        #accept or deny challenge
        elif 'answer_challenge' in request.POST:
            if 'accept' in request.POST:
                return redirect('/game/?challenge=%s'%request.POST['accept'])
            elif 'deny' in request.POST:
                Challenge.objects.get(pk=request.POST['deny']).delete()


        #start a new game
        elif "start_game" in request.POST:
            return redirect("/game/?new_game=1")

        #continue a game
        elif "continue_game" in request.POST:
            return redirect("/game/?continue_game=%d"%request.POST["continue_game"])

    #gather all challenges for player1
    challenges_player1 = []
    if request.session.get('player1', ''):
        p1 = request.session['player1']
        challenges_player1 = Challenge.objects.filter(player2=p1['pk'])

    #gather all active matches for player1
    matches_player1 = []
    if request.session.get('player1', ''):
        p1 = request.session['player1']['pk']
        matches_player1 = ChessGame.objects.filter(player_white_pk=p1) | ChessGame.objects.filter(player_black_pk=p1)

    template = 'home/index.html'
    context = {'opponent_picker_form':OpponentPicker,
                'challenges_player1':challenges_player1,
                'matches_player1':matches_player1,}
    return render_to_response(template, context, context_instance=RequestContext(request))
