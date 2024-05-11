import os
import pygame as pg
# from sprites import Card
from random import randint
from typing import List

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

### Util funcs for list of cards
def sort_cards(cards):
    if len(cards) < 2:
        return cards
    low, same, high = [], [], []
    pivot = cards[randint(0, len(cards) - 1)]
    for card in cards:
        if float(card) < float(pivot):
            low.append(card)
        elif float(card) == float(pivot):
            same.append(card)
        elif float(card) > float(pivot):
            high.append(card)
    return sort_cards(low) + same + sort_cards(high)