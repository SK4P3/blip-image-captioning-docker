from dataclasses import dataclass
import threading
from typing import List
import requests
import queue
import json
from flask import Flask, jsonify, request
from io import BytesIO
import uuid
from worker_image_capture import caption_image
from PIL import Image
import time

app = Flask(__name__)
q: "queue.Queue[Job]" = queue.Queue()
results = []

@dataclass
class Job():
    id: str
    is_finished: bool
    job_result: dict
    def run(self):
        pass

# todo refactor for list
@dataclass
class ImageCaptionJob(Job):
    img: str
    def run(self):
        res = caption_image(0, self.img)
        jobRes = {'id': self.id, 'result': res}
        results.append(jobRes)
        return jobRes


@dataclass
class ImageCaptionJobBlocking(Job):
    imgs: List[str]
    def run(self):
        res = caption_image(0, self.imgs)
        self.job_result = res
        self.is_finished = True
        jobRes = {'id': self.id, 'result': res}
        return jobRes


def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')

        item.run()

        q.task_done()


@app.route("/captionImage", methods = ['GET', 'POST'])
def captionImage():
    # Get Jobs Results
    if request.method == 'GET':
        return results
    
    # Add Job to queue and return job id
    if request.method == 'POST':
        id = uuid.uuid4().hex
        data: json = request.get_json()

        if (not 'imgurls' in data ):
            return "Please specify image urls"
        
        urls = data['imgurls']

        responses = [requests.get(url) for url in urls]
        imgs = [Image.open(BytesIO(response.content)) for response in responses]

        job = ImageCaptionJob(id, False, {}, imgs)

        q.put(job)
        

        return jsonify({"msg": "Job Started!", "id": id})


@app.route("/captionImageBlocking", methods = ['GET', 'POST'])
def captionImageBlocking():

    # Add Job to queue and return job id
    if request.method == 'POST':
        id = uuid.uuid4().hex
        data: json = request.get_json()

        if (not 'imgurls' in data ):
            return "Please specify image urls!"
        
        urls = data['imgurls']

        responses = [requests.get(url) for url in urls]
        imgs = [Image.open(BytesIO(response.content)) for response in responses]

        job = ImageCaptionJobBlocking(id, False, {}, imgs)
        q.put(job)
        
        while not job.is_finished:
            time.sleep(1)

        return jsonify({"msg": "Job finished!", "id": id, "result": job.job_result})


if __name__ =='__main__':  
    threading.Thread(target=worker, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=True)