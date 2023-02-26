from PIL import Image
import torch
from pathlib import Path
import base64
from models.blip import blip_decoder
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from tqdm import tqdm
import requests


def init_model(device):
    print("Loading Model...")
    model = blip_decoder(
        pretrained="./checkpoints/model_large_caption.pth", image_size=384, vit="large"
    )
    model.eval()
    model = model.to(device)
    print(f"\nModel to {device}")
    return model


def prepare_images(pil_images, device):
    image_size = 384
    transform = transforms.Compose(
        [
            transforms.Resize(
                (image_size, image_size), interpolation=InterpolationMode.BICUBIC
            ),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.48145466, 0.4578275, 0.40821073),
                (0.26862954, 0.26130258, 0.27577711),
            ),
        ]
    )

    t_images = [transform(img).unsqueeze(0).to(device) for img in pil_images]
    return t_images

def create_dir(directory_path):
    if not Path(directory_path).is_dir():
        Path(directory_path).mkdir(exist_ok=True)
        print(f"Directory is created {Path(directory_path).stem}")

    return Path(directory_path).stem


def download_checkpoint():
    url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth"
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    with open("checkpoints/model_large_caption.pth", "wb") as file:
        print("Downloading checkpoint...")
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    print("Checkpoint downloaded!")


def validate_model():
    if not Path("checkpoints").is_dir():
        print(f"checkpoint directory did not found.")
        create_dir("checkpoints")

    if not Path("checkpoints/model_large_caption.pth").is_file():
        download_checkpoint()


def caption_image(gpu_id, images):

    # Error if no gpu remove if you want to use CPU
    if not torch.cuda.is_available():
        raise Exception("No GPU Found!")
    
    device = torch.device(f"cuda:{gpu_id}" if torch.cuda.is_available() else "cpu")

    validate_model()

    model = init_model(device)

    captions = []

    with torch.no_grad():
        print("Captioning started")

        converted_imgs = []

        for image in images:
            converted_imgs.append(image.convert('RGB'))

        transformed_images = prepare_images(converted_imgs, device)

        for image in transformed_images:
            caption = model.generate(image, sample=False, num_beams=3, max_length=20, min_length=5)
            captions.append(caption[0])
  
    print(captions)
    print("Captioning finished!")
    return captions
    

if __name__ == "__main__":
    captions = caption_image(0, Image.open('./images/1.png'))

    print(captions)
    