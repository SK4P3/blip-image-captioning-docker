# **BLIP Image Captioning inside a Docker Container with simple API**
## **Features**
- Worker Queue
- Create Image Caption of Image by passing URL

## **API Endpoints**
- **/queue GET**
    - Get job results

- **/queue POST**
    - Post a job to the queue
    - Takes json with imgurl
    - When job is done the result will be added to the result list