# docker build --tag "mpeichatbot" .
# docker run -v db_vol:/var/lib/postgres/data/ --rm -ti mpeichatbot

# Установка базового образа
FROM archlinux:base-20231029.0.188123

# Настройка рабочей директории
WORKDIR /mpeichatbot

# Копирование файлов проекта в контейнер
COPY . /mpeichatbot

# Первичная настройка
RUN --mount=type=bind,source=db_vol,target=/var/lib/postgres/data \
    ./scripts/setup.sh

# Запуск команд при старте контейнера
CMD ./scripts/start.sh