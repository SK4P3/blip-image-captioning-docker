from dataclasses import dataclass
import threading
import requests
import queue
import json
from flask import Flask, jsonify, request
from io import BytesIO
import uuid
from worker_image_capture import caption_image
from PIL import Image

app = Flask(__name__)
q: "queue.Queue[Job]" = queue.Queue()
results = []

@dataclass
class Job():
    id: str
    def run(self):
        pass


@dataclass
class ImageCaptionJob(Job):
    img: str
    def run(self):
        res = caption_image(0, self.img)
        return {'id': self.id, 'result': res}


def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')

        jobRes = item.run()

        results.append(jobRes)
        q.task_done()


@app.route("/queue", methods = ['GET', 'POST'])
def jobs():
    # Get Active Jobs
    if request.method == 'GET':
        return results
    
    # Add Job to queue and return job id
    if request.method == 'POST':
        id = uuid.uuid4().hex
        data: json = request.get_json()

        if (not 'imgurl' in data ):
            return "Please specify an image url!"
        
        response = requests.get(data['imgurl'])
        img = Image.open(BytesIO(response.content))

        q.put(ImageCaptionJob(id, [img]))

        return jsonify({"msg": "Success!", "id": id})


if __name__ =='__main__':  
    threading.Thread(target=worker, daemon=True).start()

    app.run(host="0.0.0.0", port=5000)