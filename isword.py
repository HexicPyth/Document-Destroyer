import re
import string
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(base_path, relative_path)


path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)
words_file = open(resource_path("words.txt")).readlines()

words = [re.sub(r'\W+', '', word).lower() for word
         in words_file if len(word) >= 3]


def isword(in_word):
    if in_word in words or in_word.lower() == "a" or in_word.lower() == "i":
        return True
    elif in_word != "a" and in_word != "i":
        return False


def filter_english(in_text):
    original_words_in_text = []
    words_in_text = []
    original_word = dict(zip(words_in_text, original_words_in_text))

    for word in in_text.rsplit(" "):
        if word != '' and word != " ":
            original_words_in_text.append(word)
            words_in_text.append(re.sub(r'\W+', '', word))

    words_removed = 0
    for _ in range(0, len(words_in_text)):
        word = words_in_text[_].lower()

        if not isword(word):
            print("'"+word+"'"+" is not a word!")
            original_words_in_text[:] = (value for value in original_words_in_text if value != word)
            print(original_words_in_text)

    return ' '.join(original_words_in_text)

print(isword("I"))