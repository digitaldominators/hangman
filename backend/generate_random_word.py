import random
import urllib.request


def generate_random_word():
    # https://stackoverflow.com/a/49524775/14665310
    word_list_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(word_list_url, headers=headers)
    response = urllib.request.urlopen(req)
    long_txt = response.read().decode()
    words = long_txt.splitlines()
    return random.choice(words).lower()


if __name__ == "__main__":
    print(generate_random_word())
