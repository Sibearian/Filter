from numpy import asarray, uint8, array, int16, average, max
from PIL import Image
from photoshop.History import entry

def negetive(image, name = None):
    negetive_image = asarray(image, dtype=uint8).copy()
    negetive_image[:, :, :-1] = 255 - negetive_image[:, :, :-1]
    if name != None:
        entry(name, 1, "")
    return Image.fromarray(negetive_image, mode=image.mode)

def mul_channel(image, amount, name = None):
    channels = asarray(image, dtype=int16).copy()
    channels[:, :] = channels[:, :] * array(amount)

    channels[channels[:, :, 0] >= 255, 0] = 255
    channels[channels[:, :, 0] <=   0, 0] = 0

    channels[channels[:, :, 1] >= 255, 1] = 255
    channels[channels[:, :, 1] <=   0, 1] = 0

    channels[channels[:, :, 2] >= 255, 2] = 255
    channels[channels[:, :, 2] <=   0, 2] = 0

    channels[channels[:, :, 3] >= 255, 3] = 255
    channels[channels[:, :, 3] <=   0, 3] = 0

    if name != None:
        entry(name, 2, amount)

    return Image.fromarray(channels.astype(uint8))


def add_channel(image, amount, name = None):
    channels = asarray(image, dtype=int16).copy()
    channels[:, :] = channels[:, :] + array(amount)

    channels[channels[:, :, 0] >= 255, 0] = 255
    channels[channels[:, :, 0] <=   0, 0] = 0

    channels[channels[:, :, 1] >= 255, 1] = 255
    channels[channels[:, :, 1] <=   0, 1] = 0

    channels[channels[:, :, 2] >= 255, 2] = 255
    channels[channels[:, :, 2] <=   0, 2] = 0

    channels[channels[:, :, 3] >= 255, 3] = 255
    channels[channels[:, :, 3] <=   0, 3] = 0

    if name != None:
        entry(name, 3, amount)
        
    return Image.fromarray(channels.astype(uint8))

def greyscale(image, name = None):
    im = asarray(image).copy()
    im[:, :, :-1] = max(im[:, :, :-1])

    if name != None:
        entry(name, 4, "")
        
    return Image.fromarray(im)

def sepia(image, name = None):
    channel = asarray(image).copy()
    channel[:, :, 0] = (channel[:, :, 0] * .393) + (channel[:, :, 1] *.769) + (channel[:, :, 2] * .189)
    channel[:, :, 1] = (channel[:, :, 0] * .349) + (channel[:, :, 1] *.686) + (channel[:, :, 2] * .168)
    channel[:, :, 2] = (channel[:, :, 0] * .272) + (channel[:, :, 1] *.534) + (channel[:, :, 2] * .131)
    
    if name != None:
        entry(name, 5, "")
        
    return Image.fromarray(channel)

def brightness(image, value: int, name = None):

    if name != None:
        entry(name, 6, [value])
        
    return add_channel(image, [value] * 3 + [0])

def contrast(image, amount: list[float], name = None):

    if name != None:
        entry(name, 7, amount)
        
    return mul_channel(image, amount)

def single_channel(image, threshold, name = None):
    channel = asarray(image).copy()
    channel[:, :, :-1] = average(channel[:, :, :-1])
    print(channel)
    channel[channel[:, :, 1] <= threshold, :-1] = 0
    channel[channel[:, :, 1] >  threshold, :-1] = 255

    if name != None:
        entry(name, 8, threshold)
        
    return Image.fromarray(channel)