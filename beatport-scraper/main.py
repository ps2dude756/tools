import argparse
import requests

from bs4 import BeautifulSoup

def get_tracks(url):
    r = requests.get(url)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, 'html.parser')

    tracks_html = soup.find_all('ul', class_='bucket-items')[0].find_all('li')

    tracks = []
    for track_html in tracks_html:
        artist = ', '.join(map(lambda x: x.text, track_html.find_all('p', class_='buk-track-artists')[0].find_all('a')))
        title = track_html.find_all('span', class_='buk-track-primary-title')[0].text
        mix = track_html.find_all('span', class_='buk-track-remixed')[0].text
        url = track_html.find_all('p', class_='buk-track-title')[0].find_all('a')[0].get('href')

        tracks.append(('{0} - {1} ({2})'.format(artist, title, mix), url))

    return tracks

def main(genre_urls):
    tracks = []
    dedupe = set([])

    for genre_url in genre_urls:
        print(genre_url)
        top_100 = get_tracks('{0}/top-100'.format(genre_url))
        hype_100 = get_tracks('{0}/hype-100'.format(genre_url))

        for track in top_100 + hype_100:
            song = track[0]
            url = 'https://www.beatport.com{0}'.format(track[1])
            if song not in dedupe:
                dedupe.add(song)
                tracks.append((song, url))


    with open('results.tsv', 'w') as f:
        for track in tracks:
            f.write('{0}\t{1}\n'.format(*track))

def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('genre_urls', action='store', nargs='+', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = create_args()
    main(args.genre_urls)
