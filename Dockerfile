FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

ADD ./checkpoints /app/checkpoints
ADD ./configs /app/configs
ADD ./models /app/models
COPY ./requirements.txt /app
COPY ./*.py /app

RUN apt update && apt install build-essential -y && apt-get install manpages-dev -y \
    && pip install -r /app/requirements.txt

CMD cd /app && python main.py