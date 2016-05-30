from __future__ import absolute_import

from celery import shared_task

from views import do_move

from chess_logic.models import ChessGame

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def make_ai_move(game_id):
	cg = ChessGame.objects.get(pk=game_id)
	return 'turn: %s' % cg.turn

