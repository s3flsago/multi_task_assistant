FROM python:3.10.14-slim AS base


RUN apt-get update && apt-get install -y jq \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.10.14 AS build

RUN apt-get update && apt-get install -y unzip build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install virtualenv

RUN virtualenv venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt 


FROM base AS ready
ENV PATH="/venv/bin:$PATH" PYTHONPATH="/venv/bin:/app"
WORKDIR /app
COPY . /app
COPY --from=build /venv /venv


FROM ready AS final

RUN sed -i 's/\r$//' startup.sh && chmod +x startup.sh
CMD service
ENTRYPOINT ["bash", "startup.sh"]