#!/bin/bash
# Установка зависимостей
pacman -Suy --noconfirm && pacman -S --noconfirm \
    python \
    python-virtualenv \
    postgresql

# Настройка виртуальной среды
## python
python -m venv ./venv
. ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
## postgresql
mkdir -p /run/postgresql
chown postgres:postgres /run/postgresql -R
mkdir -p /var/lib/postgres/data/
chown postgres:postgres /var/lib/postgres/data -R
source ./.env
su - postgres -c "initdb -D /var/lib/postgres/data/ -U ${POSTGRES_USER}"