import csv
import requests
import random
from bs4 import BeautifulSoup

RUCORPORA_PREFIX = 'https://processing.ruscorpora.ru/'

RHYME_URL = 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp=JSONeyJkb2NfYXV0aG9yX2lkIjogWyLQki4g0JIuINCc0LDRj9C60L7QstGB0LrQuNC5Il19&mysent=&mysize=134347&mysentsize=0&dpp=&spp=&spd=&mydocsize=634&mode=poetic&lang=ru&sort=i_grtagging&nodia=1&text=lexgramm&ext=10&parent1=0&level1=0&lex1=&gramm1=&sem-mod1=sem&sem-mod1=semx&sem1=&form1=*%D0%BA%D0%B8%D0%B9&flags1=rhyme&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=&sem-mod2=sem&sem-mod2=semx&sem2=&form2=&flags2='


def find_rhyme(row):
    lexeme = '*' + row[-2:]
    url = RHYME_URL.format(lex1=lexeme)

    text_page = requests.request('GET', url).text

    soup = BeautifulSoup(text_page, 'lxml')
    csv_link = soup.find('a', text='CSV')

    try:
        rhyme_table = requests.request('GET', RUCORPORA_PREFIX + csv_link['href'])
    except TypeError as _:
        return 'Нет подходящей cтрочки'

    decode_content = rhyme_table.content.decode('utf-8')
    reader = csv.DictReader(
        decode_content.splitlines(),
        delimiter=';',
    )

    selected_rhyme = random.choice(list(reader))
    return selected_rhyme['Left context'] + ' ' + selected_rhyme['Center'] + selected_rhyme['Punct']
