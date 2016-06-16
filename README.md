#Chess Platform (server)
a django chess platform server that uses: 
- celery for async work (like finding best chess move when playing against AI)
- postgresql database for fast concurrent use
- channels to push data to users instead of polling
- stockfish to find best move in a given position
- supervisor to make sure the server is always running (after reboot and crashes)
- nginx to serve static files
- daphne to run the django asgi

#Installation Notes (Debian)
##Step 1:Software you need
```
apt-get redis-server supervisor python-dev python-virtualenv postgresql postgresql-contrib libpq-dev git git-core stockfish build-essential nginx libevent-dev
```
##Step 2: Set up project, users and database
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
set up the user the application will run on
```
$ sudo groupadd --system app
$ sudo useradd --system --gid app --shell /bin/bash --home /apps/chess-server chess
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
$ python manage.py migrate
$ python manage.py collectstatic
```
test the server
```
$ python manage.py runserver
```
##Step 3: Configure daphne to run your app
```
$ daphne chess.asgi:channel_layer -h 0.0.0.0 -p 8888
```
make sure  celery is always running afer reboot, crash etc with supervisor
in a terminal with root copy the config
and edit it with your paths
```
$ cp /apps/chess-server/example_configs/celery-chess.conf /etc/supervisor/conf.d/
```
in the normal terminal with your user create directory for logs
```
$ mkdir logs
$ touch logs/celery-worker.log
```
make supervisor see the changes (root terminal)
```
$ supervisorctl reread
$ supervisorctl update
```
##Step 4: Make nginx serve static files
set up nginx (root terminal)
```
$ cp /apps/chess-server/example_configs/chess.nginxconf /etc/nginx/sites-available/chess
$ ln -s /etc/nginx/sites-available/chess /etc/nginx/sites-enabled/chess
$ service nginx restart
```





