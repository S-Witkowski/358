import os
import pygame as pg
from functools import wraps
import asyncio

def load_image(*args):
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(sourceFileDir, "img", *args)
    return pg.image.load(full_path).convert_alpha()        

def transform_image_size(image, space_width, size_factor):
    image_w, image_h = image.get_size()
    image_aspect_ratio = image_w / image_h
    size = (space_width*size_factor, space_width*size_factor/image_aspect_ratio)
    return pg.transform.scale(image, size)

def load_and_transform_image(*args, space_width, size_factor):
    image = load_image(*args)
    return transform_image_size(image, space_width, size_factor)


import functools

def only_once(func):
    func._called = False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func._called:
            raise RuntimeError("This function can only be called once.")
        func._called = True
        return func(*args, **kwargs)

    return wrapper