FROM python:3
WORKDIR /usr/src/app

RUN apt-get update && apt-get install libgl1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python", "./bot.py" ]
