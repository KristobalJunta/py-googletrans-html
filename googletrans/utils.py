"""A conversion module for googletrans"""
from __future__ import print_function
import re
import json

from googletrans.constants import DEFAULT_API_KEY


def build_params(src, dest, token, fmt, **kwargs) -> dict:
    return {
        'client': 'te_lib',
        'sl': src,
        'tl': dest,
        'tk': token,
        'format': fmt,
        'v': '1.0',
        'key': DEFAULT_API_KEY,
        **kwargs,
    }


def legacy_format_json(original):
    # save state
    states = []
    text = original

    # save position for double-quoted texts
    for i, pos in enumerate(re.finditer('"', text)):
        # pos.start() is a double-quote
        p = pos.start() + 1
        if i % 2 == 0:
            nxt = text.find('"', p)
            states.append((p, text[p:nxt]))

    # replace all weired characters in text
    while text.find(',,') > -1:
        text = text.replace(',,', ',null,')
    while text.find('[,') > -1:
        text = text.replace('[,', '[null,')

    # recover state
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            j = int(i / 2)
            nxt = text.find('"', p)
            # replacing a portion of a string
            # use slicing to extract those parts of the original string to be kept
            text = text[:p] + states[j][1] + text[nxt:]

    converted = json.loads(text)
    return converted


def get_items(dict_object):
    for key in dict_object:
        yield key, dict_object[key]


def format_json(original):
    try:
        converted = json.loads(original)
    except ValueError:
        converted = legacy_format_json(original)

    return converted


def rshift(val, n):
    """python port for '>>>'(right shift with padding)
    """
    return (val % 0x100000000) >> n
