FROM python:3.8

ARG DEPLOYMENT_ENV

ENV DEPLOYMENT_ENV=${DEPLOYMENT_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$DEPLOYMENT_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
RUN poetry run python -m spacy download en_core_web_sm
COPY pizza.py /app/
ENTRYPOINT [ "poetry", "run", "python", "pizza.py" ]