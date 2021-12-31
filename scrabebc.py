#!/usr/bin/env python3


from requests import get
from re import findall
from os.path import basename
from os import chdir
from sys import argv


songre = '"value":"(https://t4.bcbits.com/stream/[^"]+)'


def fatal(message):
    print(f'[!] {message}')
    exit()


def info(message):
    print(f'[*] {message}')


def store(song):
    response = get(song)
    name = basename(song).split('?')[0]
    raw = response.content

    with open(f'./{name}.mp3', 'wb') as file:
        file.write(raw)

    info(f'wrote {name}.mp3 - {round(len(raw) / 1e6, 2)}MB')


def app(album):
    response = get(album)

    if response.status_code != 200:
        fatal(f'unable to fetch {album}')

    info(f'fetched {album}')
    info('searching for song urls...')

    songs = findall(songre, response.text)

    info(f'found {len(songs)} songs')

    for song in songs:
        store(song)

    info('finished')


if __name__ == '__main__':
    if len(argv) != 3:
        fatal('usage: scrapebc.py <album url> <save path>')

    album, path = argv[1:]
    chdir(path)
    app(album)
