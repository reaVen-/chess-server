"""chess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView

from socketio import sdjango
sdjango.autodiscover()

urlpatterns = [
    url(r'^$', "home.views.index", name="index"),
    url(r'^game/poll/', "chess_logic.views.poll", name="poll"),
    url(r'^game/', "chess_logic.views.game", name="game"),
    url(r'^ai/poll/', "chess_logic.views.ai_poll", name="ai_poll"),
    url(r'^ai/', "chess_logic.views.ai", name="ai"),
    url(r'^beat/', "home.views.beat", name="beat"),
    url(r'^socket\.io', include(sdjango.urls)),
    url(r'^echo/', TemplateView.as_view(template_name='chess_logic/templates/index.html'),
        name='inde'),
]
