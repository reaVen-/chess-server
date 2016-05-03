from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from home.models import ChessUser
from django import forms

import hashlib

class OpponentPicker(forms.Form):
    choices = []
    for user in ChessUser.objects.all():
        choices.append((user.pk, user.username))
    opponents = forms.ChoiceField(choices=choices)

def login_or_create_user(username, password):
    #check if user is in database
    try:
        user = ChessUser.objects.get(username=username)
        print "HHHHHEEEEERRRREEEE"
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
            request.session['player1'] = ""
        #logout player 2
        elif 'logout_user_2' in request.POST:
            request.session['player2'] = ""

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
            password = hashlib.sha224(password)
            user = login_or_create_user(username, password)

            if user: request.session['player2'] = {'username':user.username, 'pk':user.pk}

        #start a new game
        elif "start_game" in request.POST:
            return redirect("/game/?new_game=1")

        #continue a game
        elif "continue_game" in request.POST:
            return redirect("/game/?continue_game=%d"%request.POST["continue_game"])

    template = 'home/index.html'
    context = {'opponent_picker_form':OpponentPicker,}
    return render_to_response(template, context, context_instance=RequestContext(request))
