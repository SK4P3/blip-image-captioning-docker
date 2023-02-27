# **BLIP Image Captioning inside a Docker Container with simple API**
## **Features**
- Worker Queue
- Create Image Caption of Image by passing URL

## **API Endpoints**
- **/captionImage GET**
    - Get job results

- **/captionImage POST**
    - Post a job to the queue
    - Takes json with imgurls  (urls seperated by ',')
    - When job is done the result will be added to the result list

- **/captionImageBlocking POST**
    - Post a job to the queue
    - Takes json with imgurls (urls seperated by ',')
    - Waits for job to finish and returns the result in the response


## **Setup/Installation**
- I assume that you have docker installed and a CUDA capable GPU
- I suggest that you run everything locally first to verify that every thing works as the docker image build can take quite long
- After running it locally for the first time, there should be a /checkpoints folder with the BLIP model
    - So the docker container can copy it and doesnt need to download it again

## Example

### **POST /captionImage**
**Request:**
```
{
    "imgurl": "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1600"
}
```
**Response:**
```
{
    "id": "4fbc68319cd6491daf7451139f58b6c7",
    "msg": "Job Started!"
}
```
### **POST /captionImageBlocking**
**Request:**
```
{
    "imgurl": "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1600,https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&w=1600,"
}
```
**Response:**
```
{
    "id": "93496917b71b44d49138cab7e4c5451d",
    "msg": "Job finished!",
    "result": [
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow",
        "a black and white cat sitting in the snow"
    ]
}
```
### **GET /captionImage**
**Response:**
```
[
    {
        "id": "4fbc68319cd6491daf7451139f58b6c7",
        "result": [
            "a white kitten with blue eyes sitting on a leopard print blanket"
        ]
    }
]
```