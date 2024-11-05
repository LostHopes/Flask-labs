FROM python:latest

WORKDIR /labs

ENV VIRTUAL_ENV=/labs/.env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml poetry.lock /labs/

RUN pip install --upgrade pip \
    && pip install poetry \
    && python -m venv $VIRTUAL_ENV \
    && poetry config virtualenvs.path "$VIRTUAL_ENV" \
    && poetry install --without dev

COPY . /labs/

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["src/run.py"]
