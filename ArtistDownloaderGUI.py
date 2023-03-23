from customtkinter import *
import requests
from bs4 import BeautifulSoup as bs
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import threading

class MuzikMp3Indir:
    def __init__(self, link, artist):
        self.link = link
        self.artist = artist
        self.all_links = []
        self.musics = []
        self.get_all_site_links(self.link)


    def get_all_site_links(self, link):
        r = requests.get(link)
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

    def get_all_music_links(self):
        for link in self.all_links:
            r = requests.get(link[0])

            soup = bs(r.content, 'html.parser')
            player = soup.find('audio', attrs={'id': 'player2'})
            self.musics.append({link[1]: player['src']})
        return self.musics

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


artist_pages = {'A': 'https://muzikmp3indir.com/sanatcilar-a-1', 'B': 'https://muzikmp3indir.com/sanatcilar-b-1', 'C': 'https://muzikmp3indir.com/sanatcilar-c-1', 'Ç': 'https://muzikmp3indir.com/sanatcilar-cc-1', 'D': 'https://muzikmp3indir.com/sanatcilar-d-1', 'E': 'https://muzikmp3indir.com/sanatcilar-e-1', 'F': 'https://muzikmp3indir.com/sanatcilar-f-1', 'G': 'https://muzikmp3indir.com/sanatcilar-g-1', 'H': 'https://muzikmp3indir.com/sanatcilar-h-1', 'I': 'https://muzikmp3indir.com/sanatcilar-ii-1', 'İ': 'https://muzikmp3indir.com/sanatcilar-i-1', 'J': 'https://muzikmp3indir.com/sanatcilar-j-1', 'K': 'https://muzikmp3indir.com/sanatcilar-k-1', 'L': 'https://muzikmp3indir.com/sanatcilar-l-1', 'M': 'https://muzikmp3indir.com/sanatcilar-m-1', 'N': 'https://muzikmp3indir.com/sanatcilar-n-1', 'O': 'https://muzikmp3indir.com/sanatcilar-o-1', 'Ö': 'https://muzikmp3indir.com/sanatcilar-oo-1', 'P': 'https://muzikmp3indir.com/sanatcilar-p-1', 'Q': 'https://muzikmp3indir.com/sanatcilar-q-1', 'R': 'https://muzikmp3indir.com/sanatcilar-r-1', 'S': 'https://muzikmp3indir.com/sanatcilar-s-1', 'Ş': 'https://muzikmp3indir.com/sanatcilar-ss-1', 'T': 'https://muzikmp3indir.com/sanatcilar-t-1', 'U': 'https://muzikmp3indir.com/sanatcilar-u-1', 'Ü': 'https://muzikmp3indir.com/sanatcilar-uu-1', 'V': 'https://muzikmp3indir.com/sanatcilar-v-1', 'W': 'https://muzikmp3indir.com/sanatcilar-w-1', 'X': 'https://muzikmp3indir.com/sanatcilar-x-1', 'Y': 'https://muzikmp3indir.com/sanatcilar-y-1', 'Z': 'https://muzikmp3indir.com/sanatcilar-z-1', '1': 'https://muzikmp3indir.com/sanatcilar-1-1', '2': 'https://muzikmp3indir.com/sanatcilar-2-1', '3': 'https://muzikmp3indir.com/sanatcilar-3-1', '4': 'https://muzikmp3indir.com/sanatcilar-4-1', '5': 'https://muzikmp3indir.com/sanatcilar-5-1', '6': 'https://muzikmp3indir.com/sanatcilar-6-1', '7': 'https://muzikmp3indir.com/sanatcilar-7-1', '8': 'https://muzikmp3indir.com/sanatcilar-8-1', '9': 'https://muzikmp3indir.com/sanatcilar-9-1'}
artist_url = ''
artist_name= ''
root = CTk()
root.title('Artist Downloader')
root.geometry('700x500')

def clean(word):
	word = word.replace(' ','')
	word = word.replace('\n', '')
	word = word.lower()
	return word

def list_album(album_url):
	muzikmp3indir = MuzikMp3Indir(album_url, artist_name)
	musics = muzikmp3indir.get_all_music_links()
	print(musics)

def show_albums(albums):
	row = 0
	col = 0
	albums_frame.pack()
	for widget in albums_frame.winfo_children():
	    widget.destroy()
	for album in albums:
		try:
			raw_data = requests.get(album['album_thumbnail'])
			im = Image.open(io.BytesIO(raw_data.content))
			image = CTkImage(im, size=(150,150))
			label1 = CTkButton(albums_frame, text='', image=image, command= lambda: list_album(album['album_url'])).grid(row=row, column=col, padx=15)
			label = CTkLabel(albums_frame, text=album['album_title']).grid(row=row+1, column=col, padx=15)
			if col<4:
				col+=2
			else:
				row+=2
				col = 0
		except Exception as e:
			print(e)
	im = Image.open('images/artist-downloader.png')
	image = CTkImage(im, size=(150,150))
	label1 = CTkButton(albums_frame, text='', image=image, command= lambda: list_album(artist_url)).grid(row=row, column=col, padx=15)
	label = CTkLabel(albums_frame, text="All songs").grid(row=row+1, column=col, padx=15)
	col+=2

def collect_albums(url):
	r = requests.get(url).content
	soup = bs(r, 'html.parser')
	items = soup.find('div', attrs= {'class': 'list'}).find_all('div', 
		attrs={'class': 'list-item'})
	albums = []
	for item in items:
		album_url = item.find('a')['href']
		album_thumbnail = item.find('img')['src']
		# print(album_thumbnail)
		album_title = item.find('strong', attrs={'class': 'title'}).text
		albums.append({'album_title': album_title, 'album_url': album_url, 'album_thumbnail': album_thumbnail})
	show_album_thread = threading.Thread(target = show_albums, args=(albums,))
	show_album_thread.start()

def search_artist():
	global artist_url, artist_name
	artist_name = artist_name_entry.get()
	link_to_search = artist_pages[artist_name[0].upper()]
	r = requests.get(link_to_search)
	soup = bs(r.content, 'html.parser')
	artists = soup.find_all('a', attrs={'class': 'singers'})
	artist_url = ''
	for i in artists:
		if clean(artist_name) == clean(i.find('div').text):
			artist_url = i['href']
			artist_name = i.find('div').text
	if not artist_url:
		messagebox.showerror('Not Found', 'Your Artist not found on muzikmp3indir.com')
	else:
		collect_albums(artist_url)

label = CTkLabel(master=root, text="Please Enter name of Artist:").pack()

artist_name_entry = CTkEntry(master=root)
artist_name_entry.pack()

button = CTkButton(master=root, text="Search Artist", command = search_artist).pack()

albums_frame = CTkScrollableFrame(master=root, width=600, height=400)



root.mainloop()