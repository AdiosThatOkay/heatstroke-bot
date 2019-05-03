FROM python:3
RUN groupadd -r heatstroke && useradd -r -g heatstroke heatstroke
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY --chown=heatstroke:heatstroke bot.py /app/bot.py
COPY --chown=heatstroke:heatstroke hsbot /app/hsbot
COPY --chown=heatstroke:heatstroke manage.py /app/manage.py
COPY --chown=heatstroke:heatstroke tests /app/tests

EXPOSE 5000
USER heatstroke
ENV TZ=Asia/Tokyo
ENV LINE_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
ENV LINE_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

RUN python manage.py init_db && python manage.py insert_observatories
RUN python -m unittest discover tests

VOLUME ["/app/hsbot/database"]
ENTRYPOINT ["python", "bot.py"]
