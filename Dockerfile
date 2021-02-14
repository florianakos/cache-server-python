FROM python:3.8-alpine3.13

WORKDIR /app

COPY requirements.txt .

RUN addgroup -S app \
    && adduser -D  -u 1000 app -G app \
    && apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .pynacl_deps gcc musl-dev \
    && rm requirements.txt

COPY --chown=app:app src/ src/

USER app

ENTRYPOINT [ "python" ]
CMD [ "src/app.py" ]
