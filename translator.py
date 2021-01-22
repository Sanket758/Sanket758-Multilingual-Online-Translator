import requests as re
from bs4 import BeautifulSoup
# import argparse
import sys

# parser = argparse.ArgumentParser(description="This program translates a given word into different language")
#
# parser.add_argument("-sr", "--source_language", choices=['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
#                                                           'Japanese','Dutch', 'Polish', 'Portuguese', 'Romanian',
#                                                           'Russian', 'Turkish'],
#                     help="Source language for the translation")
#
# parser.add_argument("-tr", "--target_language", choices=['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
#                                                           'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian',
#                                                           'Russian', 'Turkish'],
#                     help="Target language for the translation")
#
# parser.add_argument("-inp", "--input_word", help="Input word to be translated")
#
# args = parser.parse_args()

# print("Hello, you're welcome to the translator. Translator supports:")
supported_langs = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                   'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

# for i, lang in enumerate(supported_langs):
#     print(f'{i + 1}. {lang}')

# src_language = int(input('Type the number of your language:\n>')) - 1
# trg_language = int(input('Type the number of language you want to translate to:\n>')) - 1
# word = input('Type the word you want to translate:\n>').lower()

# src_language = int(args.source_language) - 1
# trg_language = int(args.target_language) - 1
# word = args.input_word.lower()

src_language = sys.argv[1].lower()
trg_language = sys.argv[2].lower()
word = sys.argv[3].lower()


# def create_url(Source_Lang, Targ_Lang):
#     baseurl = 'https://context.reverso.net/translation/'
#     urlheaders = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
#     baseurl += f'{supported_langs[Source_Lang].lower()}-{supported_langs[Targ_Lang].lower()}/'
#     return baseurl, urlheaders

def create_url(Source_Lang, Targ_Lang):
    if Targ_Lang.capitalize() not in supported_langs:
        print(f"Sorry, the program doesn't support {Targ_Lang}")
        sys.exit(0)
    baseurl = 'https://context.reverso.net/translation/'
    urlheaders = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    baseurl += f'{Source_Lang}-{Targ_Lang}/'
    return baseurl, urlheaders


def get_translated_words(soupobj):
    return [data.text.strip() for data in soupobj.select('#translations-content a')][:5]


def get_translated_examples(soupobj):
    trans_source_examples = [data.text.strip() for data in soupobj.select('#examples-content .example .src ')]
    while '' in trans_source_examples:
        trans_source_examples.remove('')

    trans_target_examples = [data.text.strip() for data in soupobj.select('#examples-content .example .trg ')]
    while '' in trans_target_examples:
        trans_target_examples.remove('')

    return trans_source_examples, trans_target_examples


s = re.Session()

if trg_language == 'all':
    with open(f'{word}.txt', 'w') as f:
        lang_list = supported_langs
        lang_list.remove(src_language.capitalize())
        for i in range(len(lang_list)):
            url, headers = create_url(src_language, lang_list[i].lower())
            query = url + word

            try:
                res = s.get(query, headers=headers)
            except re.exceptions.ConnectionError:
                print('Something wrong with your internet connection')
                sys.exit(0)

            soup = BeautifulSoup(res.content, 'html.parser')

            trans_words = get_translated_words(soup)

            if len(trans_words) < 1:
                print(f'Sorry, unable to find {word}')
                sys.exit(0)

            print(f'\n{supported_langs[i].capitalize()} Translations:')
            for w in trans_words:
                print(w)
            print(f'\n{supported_langs[i]} Examples:')
            source_examples, target_examples = get_translated_examples(soup)
            print(source_examples[0])
            print(target_examples[0])
            f.write(f'{supported_langs[i]} Translations:\n')
            # print(len(trans_words))
            for w in trans_words:
                f.write(w + '\n')
            # f.write(trans_words[0] + '\n')
            f.write(f'\n{supported_langs[i]} Examples:\n')
            f.write(source_examples[0] + '\n')
            f.write(target_examples[0] + '\n\n')
else:
    url, headers = create_url(src_language, trg_language)
    query = url + word

    try:
        res = s.get(query, headers=headers)
    except re.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit(0)

    soup = BeautifulSoup(res.content, 'html.parser')
    trans_words = get_translated_words(soup)

    if len(trans_words) < 1:
        print(f'Sorry, unable to find {word}')
        sys.exit(0)

    # print(f'\n{supported_langs[trg_language]} Translations:')
    print(f'{trg_language.capitalize()} Translations:')
    for w in trans_words:
        print(w)
    # print(trans_words[0])
    # print(f'\n{supported_langs[trg_language]} Examples:')
    print(f'\n{trg_language.capitalize()} Examples:')

    source_examples, target_examples = get_translated_examples(soup)
    for i in range(5):
        print(source_examples[i])
        print(target_examples[i] + '\n')

    with open(f'{word}.txt', 'w') as f:
        f.write(f'{trg_language.capitalize()} Translations:\n')
        for w in trans_words:
            f.write(w + '\n')
        f.write(f'\n{trg_language.capitalize()} Examples:\n')
        for i in range(5):
            f.write(source_examples[i] + '\n')
            f.write(target_examples[i] + '\n\n')


'''
    *** Please tell me who you are. Run git config --global user.email "you@example.com" 
    git config --global user.name "Your Name" 
    to set your account's default identity. 
    Omit --global to set the identity only in this repository. 
    unable to auto-detect email address (got 'sanket@sanket-Latitude-E7440.(none)')
'''