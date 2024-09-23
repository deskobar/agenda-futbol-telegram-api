FROM python:3.10.9

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==1.4.2"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

ENV PORT=8080

EXPOSE 8080

ENTRYPOINT ["poetry", "run"]

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
