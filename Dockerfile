FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

COPY ./checkpoints /app
COPY ./configs /app
COPY ./models /app
COPY ./requirements.txt /app
COPY ./*.py /app

RUN apt update && apt install build-essential -y && apt-get install manpages-dev -y \
    && pip install -r /app/requirements.txt

CMD python /app/main.py