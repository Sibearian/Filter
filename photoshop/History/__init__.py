import sqlite3
from PIL import Image
from pandas import DataFrame

connection = sqlite3.connect("images.db")
DB = connection.cursor()

DB.execute('create table images(file_name varchar(200), value varchar(50), operation int);')
connection.commit()

def entry(fn : str, operation : int, values : str | list):
    if values == "":
        value = ""
    else:
        value = ",".join(map(lambda x: str(x), values))

    DB.execute(f"Insert into images(file_name, value, operation) values ('{fn}', '{value}', {operation});")
    connection.commit()
    DB.execute('Select * from images')
    print(DB.fetchall())

def undo(fn, steps):
    from photoshop import Filters
    DB.execute(f"Select * from images where file_name = '{fn}';")
    operations = DB.fetchall()
    if len(operations) < steps:
        return Image.open(fn)
    
    operations = operations[:-steps]
    image = Image.open(fn)

    for operation in operations:
        if operation[-1] == 1:
            image = Filters.negetive(image)
        if operation[-1] == 2:
            image = Filters.mul_channel(image, [int(x) for x in operation[1].split(",")])
        if operation[-1] == 3:
            image = Filters.add_channel(image, [int(x) for x in operation[1].split(",")])
        if operation[-1] == 4:
            image = Filters.greyscale(image)
        if operation[-1] == 5:
            image = Filters.sepia(image)
        if operation[-1] == 6:
            image = Filters.brightness(image, int(operation[1]))
        if operation[-1] == 7:
            image = Filters.contrast(image, [int(x) for x in operation[1].split(",")])
        if operation[-1] == 8:
            image = Filters.single_channel(image, operation[1])

    return image

def get_operation(value : int) -> str:
    if   value == 1:
        return 'negetive'
    elif value == 2:
        return 'mul_channel'
    elif value == 3:
        return 'add_channel'
    elif value == 4:
        return 'greyscale'
    elif value == 5:
        return 'sepia'
    elif value == 6:
        return 'brightness'
    elif value == 7:
        return 'contrast'
    return 'single_channel'

def get_dataframe(fn : str):
    DB.execute("select * from images;")
    data = list(filter(lambda x : True if x[0] == fn else False, DB.fetchall()))
    return DataFrame(data, columns=["File Name", "Values used", "Operation"])