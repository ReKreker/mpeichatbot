source ./.env
su - postgres -c "pg_ctl -D /var/lib/postgres/data/ start"
. ./venv/bin/activate
./venv/bin/python main.py