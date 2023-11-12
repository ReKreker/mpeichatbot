source ./.env
su - postgres -c "pg_ctl -D /var/lib/postgres/data/ start"
su - postgres -c "createdb -h localhost -p 5432 -U ${POSTGRES_USER} ${POSTGRES_DATABASE}"
. ./venv/bin/activate
./venv/bin/python main.py