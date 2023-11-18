FROM python:3.11

WORKDIR /simple_web

COPY . .

VOLUME [ "/simple_web/storage" ]

EXPOSE 3000 5000

ENTRYPOINT [ "python3", "main.py"]