FROM python:3.10-slim

RUN mkdir autofl-ui
WORKDIR  /autofl-ui
COPY pyproject.toml /autofl-ui

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-ansi
COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
RUN dir -s
ENTRYPOINT ["streamlit", "run", "/autofl-ui/src/Main.py", "--server.port=8501", "--server.address=0.0.0.0"]