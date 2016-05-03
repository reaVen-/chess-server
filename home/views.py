from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def index(request):
    if "start_game" in request.POST:
        return redirect("/game/?new_game=1")
    template = 'index.html'
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))
