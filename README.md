# soa_mafia
Mafia (Werewolves) game on Python

### Запуск игры
Сервер можно запустить локально или в докере:

- **Локально**
  1. Установить необходимые пакеты
     ```
     pip3 install -r requirements.txt
     ```
  2. Отредактировать конфиг по пути ```game_config.py``` (если требуется).
  3. Запустить:
     ```python3 server.py```
- **Docker**
    - Собрать image
        ```
        docker build -t mafia/game . -f Dockerfile
        ```

    - Запустить собранный image в контейнере
        ```
        docker run -d -p ${YOUR_PORT}:${YOUR_PORT} --name mafia -t mafia/game
        ```

Клиент запускается локально:
 1. Установить необходимые пакеты
     ```
     pip3 install -r requirements.txt
     ```
 2. Запустить:
     ```python3 client.py```

### Игра
Игра начинается, когда к серверу подключается `PLAYERS_COUNT` в конфиге (`game_config.py`) количество человек.

Количество мафий равно одной трети от игроков с округлением в меньшую сторону. Полицейский в игре один.

Игра начинается c хода мафии, потом просыпается полицейский.
После конца игры, можно проголосовать за еще одну, чтобы она началась нужна готовность всех игроков.
