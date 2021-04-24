FROM python:slim

WORKDIR /src
COPY src .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]