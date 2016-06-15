#Chess Platform (server)
This is a chess platform you can host on your own computer

#Installation Notes (Debian)
##Step 1:Software you need
```
apt-get redis-server supervisor python-dev python-virtualenv postgresql postgresql-contrib libpq-dev git git-core stockfish build-essential nginx
```
##Step 2: Set up users and database
log in to postgres user and create a new database and a database user
```
$ su postgres
$ createuser --interactive -P
Enter name of role to add: chess
Enter password for new role:
Enter it again: 
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n

$ createdb --owner chess chessdb
$ logout
```
set up project directory
```
$ mkdir /apps/
$ chown chess /apps/

$ su - chess
$ cd /apps
$ git clone https://github.com/reaVen-/chess-server.git
$ cd chess-server
$ virtualenv .
$ source bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```
configure django with your database
```
$ cp example_configs/local_settings.py chess
$ nano chess/local_settings.py
```
build the initial database
```
$ python manage.py migrate --settings=chess.local_settings
```
test the server
```
$ python manage.py runserver --settings=chess.local_settings
```
set up a gunicorn start script (change paths in gunicorn_start)
```
$ cp example_configs/gunicorn_start bin
$ nano bin/gunicorn_start
$ chmod u+x bin/gunicorn_start
```
make sure gunicorn and celery is always running afer reboot, crash etc with supervisor
in a terminal with root copy the config
and edit it with your paths
```
$ cp /apps/chess-server/example_configs/gunicorn-chess.conf /etc/supervisor/conf.d/
$ cp /apps/chess-server/example_configs/celery-chess.conf /etc/supervisor/conf.d/
```
in the normal terminal with your user create directory for logs
```
$ mkdir logs
$ touch logs/gunicorn_supervisor.log
$ touch logs/celery-worker.log
```
make supervisor see the changes (root terminal)
```
$ supervisorctl reread
$ supervisorctl update
```
set up nginx (root terminal)
```
$ cp /apps/chess-server/example_configs/chess.nginxconf /etc/nginx/sites-available/chess
$ ln -s /etc/nginx/sites-available/chess /etc/nginx/sites-enabled/chess
$ service nginx restart
```





