from __future__ import absolute_import

from celery import shared_task

from chess_logic.models import ChessGame

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def make_ai_move(request):
	return 'turn: %s' % request.session['player1']['username']

