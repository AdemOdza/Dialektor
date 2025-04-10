FROM python:3.12.9-bookworm

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV FLASK_APP=src.server.py:app
ENV FLASK_ENVIRONMENT=development

EXPOSE 3000

WORKDIR /dialektor

COPY pyproject.toml ./
COPY poetry.lock ./
ADD src ./src

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH=/root/.local/bin:$PATH

RUN poetry install

CMD ["poetry", "run", "python", "src/server.py"]