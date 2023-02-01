from PIL import Image
from photoshop.History import get_dataframe

def load_image(file_name : str):
    image = Image.open(file_name)
    return (image, file_name)

def load_images(file_names : list[str]):
    images = []
    for file in file_names:
        t = Image.open(file)
        images.append(t)
        if images != None:
            if images[0].mode != t.mode:
                raise Exception("Not of same file type")
    return (images, file_names)

def save_image(file_name : str, image):
    image.save(f"{file_name}.png")

def save_images(images : dict):
    for file_name, image in images.items():
        image.save(f'{file_name}.png')

def save_history(csv_name : str, file_name : str):
    history = get_dataframe(file_name)
    history.to_csv(csv_name, index=False)