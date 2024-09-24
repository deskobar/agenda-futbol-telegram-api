FROM python:3.10.9

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==1.4.2"

COPY poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN poetry install --no-root

COPY . .

# Change ownership of the app directory to the non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser && chown -R appuser:appuser /app
# Switch to non-root user
USER appuser

ENV PORT=8080

EXPOSE ${PORT}

CMD poetry run uvicorn api.app:app --host 0.0.0.0 --port $PORT
