# Установка базового образа
FROM archlinux:base-20231029.0.188123

# Настройка рабочей директории
WORKDIR /mpeichatbot

# Копирование файлов проекта в контейнер
COPY . /mpeichatbot

# Установка зависимостей
RUN pacman -Suy --noconfirm && pacman -S --noconfirm \
    python \
    python-virtualenv \
    postgresql
RUN python -m venv /mpeichatbot/venv
RUN . /mpeichatbot/venv/bin/activate && /mpeichatbot/venv/bin/pip install -r /mpeichatbot/requirements.txt
RUN su - postgres -c 'initdb -D /var/lib/postgres/data/ -U postgres'
RUN mkdir /run/postgresql
RUN chown postgres:postgres /run/postgresql -R


# Запуск команды по умолчанию
CMD su - postgres -c "pg_ctl -D /var/lib/postgres/data/ start"
CMD . /mpeichatbot/venv/bin/activate && /mpeichatbot/venv/bin/python /mpeichatbot/main.py