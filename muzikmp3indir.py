import requests, os
from bs4 import BeautifulSoup as bs


class MuzikMp3Indir:
    def __init__(self, link, artist):
        self.link = link
        self.artist = artist
        self.all_links = []
        self.create_folder()
        self.get_all_site_links(self.link)
        print(len(self.all_links))
        self.get_all_music_links(self.all_links)

    def create_folder(self):
        try:
            os.mkdir(self.artist)
        except FileExistsError:
            print('[FileExistsError]')

    def get_all_site_links(self, link):
        r = requests.get(link)
        print(link)
        soup = bs(r.content, 'html.parser')
        links = soup.find('div', attrs={'class': 'episodes'})
        for i in links:
            links = i.find_all_next('div', attrs={'class': 'col-10'})
            for n in links:
                filename = n.find('div', attrs={'class': 'artist'}).text.replace('\n','')+' - '+n.find('div', attrs={'class': 'song'}).text.replace('\n','')
                elem = [n.find('a')['href'],filename]
                if elem not in self.all_links:
                    self.all_links.append(elem)
        next_link = soup.find('a', attrs={'rel': 'next'})
        # print(len(next_link))
        if next_link:
            self.get_all_site_links(next_link['href'])

    def get_all_music_links(self, links):
        for link in links:
            r = requests.get(link[0])
            # print(dir(r))
            # print(link)
            soup = bs(r.content, 'html.parser')
            player = soup.find('audio', attrs={'id': 'player2'})
            self.download_file(player['src'], link[1])

    def download_file(self, url, filename):
        filename = filename.replace('?', '')
        path = self.artist+'/'+filename+'.mp3'
        if not os.path.isfile(path):
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): 
                            f.write(chunk)
                print('[DOWNLOADED]', path)
            except:
                print('[HTTPError]')
        else:
            print('[EXISTS]',path)


Artists = [
    ['https://muzikmp3indir.com/sanatci-8347-worry-mp3-indir', 'Worry'],
]

for artist in Artists:
    muzik = MuzikMp3Indir(artist[0], artist[1])
