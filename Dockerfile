FROM python:latest

COPY ./mafia_server.py .
COPY ./mafia_commands.py .
COPY ./game_config.py .
COPY ./proto ./proto

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "mafia_server.py"]
