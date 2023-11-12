# docker build --tag "mpeichatbot" .
# docker run -v ./postgresql_db:/var/lib/postgres/data/ --rm -ti mpeichatbot

# Установка базового образа
FROM archlinux:base-20231029.0.188123

# Настройка рабочей директории
WORKDIR /mpeichatbot

# Копирование файлов проекта в контейнер
COPY . /mpeichatbot

# Первичная настройка
RUN ./scripts/setup.sh

# Запуск команд при старте контейнера
CMD ./scripts/start.sh