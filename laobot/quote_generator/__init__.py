import os
import re
import markovify

from ..utils import constants


def get_file(path):
    with open(os.path.join(constants.CORPUS_DIRECTORY, path)) as infile:
        return infile.read().strip()


def get_model(path):
    data = get_file(path)
    return markovify.Text(data) if data else None


def generate_complete_model():
    targets = os.listdir(constants.CORPUS_DIRECTORY)
    models = [get_model(path) for path in targets]
    return markovify.combine([m for m in models if m])


def find_substring(substring):
    pattern = re.compile(substring, re.IGNORECASE | re.MULTILINE)
    for path in os.listdir(constants.CORPUS_DIRECTORY):
        text = get_file(path)
        if pattern.search(text):
            text_index = text.find(substring)
            return path, '...' + text[text_index-25:text_index+75] + '...'
    return False, None
