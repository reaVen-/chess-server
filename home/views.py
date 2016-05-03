from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def index(request):
    if request.method == "POST":
        #start a new game
        if "start_game" in request.POST:
            return redirect("/game/?new_game=1")
        elif "continue_game" in request.POST:
            return redirect("/game/?continue_game=%d"%request.POST["continue_game"])

    template = 'home/index.html'
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))
