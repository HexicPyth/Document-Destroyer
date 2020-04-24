from mtranslate import translate
import random as insecure_random
from urllib import error
import isword

random = insecure_random.SystemRandom()  # make random() Cryptographically-Secure.

# Languages and their two-letter codes(e.x: en, es) which are supported by Google Translate
language_codes = ["af", "sq", "ar", "az", "eu", "bn", "be", "bg", "ca", "zh-CN", "zh-TW", "hr",
                  "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "gl", "ka", "de", "el",
                  "gu", "ht", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "kn", "ko", "la",
                  "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk",
                  "sl", "es", "sw", "ta", "te", "th", "tr", "uk", "ur", "vi", "cy", "yi"]
languages = ["Afrikaans", "Albanian", "Arabic", "Azerbaijani", "Basque", "Bengali",
             "Belarusian", "Bulgarian", "Catalan", "Chinese Simplified", "Chinese Traditional",
             "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian",
             "Filipino", "Finnish", "French", "Galician", "Georgian", "German", "Greek",
             "Gujarati", "Haitian Creole", "Hebrew", "Hindi", "Hungarian", "Icelandic",
             "Indonesian", "Irish", "Italian", "Japanese", "Kannada", "Korean", "Latin",
             "Latvian", "Lithuanian", "Macedonian", "Malay", "Maltese", "Norwegian",
             "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak",
             "Slovenian", "Spanish", "Swahili", "Swedish", "Tamil", "Telugu", "Thai",
             "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh", "Yiddish"]

complete_layers = 0


def find_substring(in_string, substring):
    start = 0
    while True:
        start = in_string.find(substring, start)
        if start == -1: return
        yield start
        start += len(substring)  # use start += 1 to find overlapping matches


def split_by_sentence(in_string, punctuation):
    sentences = []
    indexes = [0]
    amount_of_sentences = 0
    for delimiter in punctuation:
        temp_sentences = list(find_substring(in_string, delimiter))
        if len(temp_sentences) != 0:
            amount_of_sentences += 1
    print("Found " + str(amount_of_sentences) + " sentences!")
    if amount_of_sentences == 0:
        in_string += random.choice([".", "!", "?"])  # Input string doesn't practice good grammar. Give it punctuation.
        print("Whoever made this message doesn't practice proper english. Added a random punctuation symbol to end of"
              " sentence...")

    for delimiter in punctuation:
        for i in list(find_substring(in_string, delimiter)):
            if i != 0:
                print("Found " + delimiter + " at " + str(i))
                indexes.append(i + 1)
    i = 0
    # Oops, range(0,indexes) would be more appropriate here... :|
    for index in indexes:
        try:
            start = indexes[i]
            end = indexes[i + 1]
            sentence = in_string[start:end]
            if sentence != '':
                print(sentence)
                sentences.append(sentence)
                i += 1

        except IndexError:
            # Reached end of indexes list... --> not a critical problem :)
            print("split_by_sentences() encountered an IndexError...")
            i += 1

    return sentences


def make_my_text_weird(in_text, layers, show_intermediate_translations=False, verbose=False, i_am_a_wimp=False,
                       progress_text=None, UI=None, original_sentence_count=None, fast_mode=False):
    global complete_layers
    """Translate some text through many layers of translation and return the output.
    Warning: Output may be explicit or otherwise false or unjust.
    I am not responsible for any action that occur as a result of this function.
    You have been warned.
    Also, This software is licenced under an MIT License. Copyright HexicPyth 2018"""

    global language_codes
    global languages
    global complete_layers
    current_text = in_text

    you_are_a_wimp = i_am_a_wimp

    if you_are_a_wimp:
        cont = input("Warning: The Following stage will access the Google Translate API (Illegally) Continue? (y/n)")

        if cont == "y" or cont == "Y" or cont == "yes":
            pass
        else:
            return None

    completed_layers = 0

    for i in range(0, layers):
        language_code = random.choice(language_codes)
        intermediate_language = languages[language_codes.index(language_code)]

        try:
            current_text = translate(current_text, language_code)

        except error.HTTPError:

            if UI and progress_text and original_sentence_count:
                import tkinter
                UI.update()
                progress_text.delete(1.0, tkinter.END)
                progress_text.insert(tkinter.END, "Oops, an error occurred :(")
                UI.update()
            print("Error: Text too long.")

            print(len(current_text))
            language_code = random.choice(language_codes)
            # 2000 is a magic number. For some reason, text sizes under 2000 (almost) never fail! I don't know why.
            current_text = translate(current_text[:2000], language_code)

        completed_layers += 1
        complete_layers += 1

        if show_intermediate_translations:
            print(current_text)

        if verbose:
            if fast_mode:
                status_string = str(round((completed_layers / layers), 2) * 100) + "% complete"
                print(status_string)
                import tkinter
                UI.update()
                progress_text.delete(1.0, tkinter.END)
                progress_text.insert(tkinter.END, status_string)
                UI.update()

            if UI and progress_text and original_sentence_count and not fast_mode:
                total_layers = (layers * 2) + (layers * original_sentence_count)
                print("Total Layers:" + str(total_layers))
                percent_complete = round(complete_layers / total_layers, 2) * 100
                status_string = str(percent_complete)[:5] + "% complete"
                print(complete_layers)
                print(status_string)
                import tkinter
                UI.update()
                progress_text.delete(1.0, tkinter.END)
                progress_text.insert(tkinter.END, status_string)
                UI.update()

    out_text = translate(current_text[:4999], "en")
    return out_text


def slow_translate(in_text, layer_count, intermediate=False, verbose=False, wimpiness=False, progress_text=None,
                   UI=None):
    global complete_layers
    complete_layers = 0

    # 1. Initial Translation of [layer_count] Layers
    # 2. Translate each sentence [layer_count] times
    # 3. Final Translation of [layer_count] layers
    # So basically a translation sandwich; sounds yummy :P

    original_sentence_count = len(split_by_sentence(in_text, ["!", ".", "?"]))

    # Translate Input
    preformat_translation = make_my_text_weird(in_text, layer_count, intermediate, verbose, wimpiness,
                                               progress_text=progress_text, UI=UI,
                                               original_sentence_count=original_sentence_count)

    sentences = split_by_sentence(preformat_translation, ["!", ".", "?"])
    print("Sentences: " + str(sentences))

    # I'm lazy and this loop wasn't working :|
    for i in range(0, 2):
        null_index = 0
        for sentence in sentences:
            if sentence == '':
                print(null_index)
                sentences.pop(null_index)
            null_index += 1

    print(sentences)

    # Translate sentences individually...
    new_sentences = [make_my_text_weird(
        sentence, layer_count, intermediate, verbose, wimpiness, progress_text=progress_text, UI=UI,
        original_sentence_count=original_sentence_count)
        for sentence in sentences]

    # Translate output
    final_output = make_my_text_weird(' '.join(new_sentences), layer_count, intermediate, verbose, wimpiness,
                                      progress_text=progress_text, UI=UI,
                                      original_sentence_count=original_sentence_count)

    complete_layers = 0
    return isword.filter_english(final_output)
