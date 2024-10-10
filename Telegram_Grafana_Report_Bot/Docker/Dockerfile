# Builder initialization:
FROM python:3.11-alpine as builder

# Dependencies tools:
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev

# Work directory:
WORKDIR /application

# Install libs:
COPY Docker/requirements.txt /application/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# System initialization:
FROM python:3.11-alpine

# Work directory:
WORKDIR /application

# Get dependencies:
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy code:
COPY /Source_code /application/Source_code
COPY /config.json /application/temporary_config.json

# Make shell entrypoint exequteble:
RUN chmod +x ./Source_code/entry_point.sh

# Run:
ENTRYPOINT ["./Source_code/entry_point.sh"]