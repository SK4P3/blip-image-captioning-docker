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

## Example

### **POST /queue**
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
    "msg": "Success!"
}
```
### **GET /queue**
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