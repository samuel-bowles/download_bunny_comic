#! python3
#download_bunny-comic.py - Downloads every single bunny-comic.

import requests
import os
import bs4

url = 'http://bunny-comic.com' # starting url
os.makedirs('bunny-comic', exist_ok=True) # store comics in ./bunny-comic
while not url == 'http://www.bunny-comic.com/1.html':
    #Download the page
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    #Find the url of the comic image
    comic_elem = soup.select('#strip a img')
    if comic_elem == []:
        print('Could not find comic image.')

    else:
        try:
            comic_url = 'http://www.bunny-comic.com/' + comic_elem[1].get('src')
            #Download the image.
            print('Downloading image %s...' % (comic_url))
            res = requests.get(comic_url)
            res.raise_for_status()

            # Save the image to ./bunny-comic
            image_file = open(os.path.join('bunny-comic', os.path.basename(comic_url)), 'wb')
            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()

        except:
            #Get the prev button's url
            prev_link = soup.select('#strip a')[0]
            url = 'http://bunny-comic.com' + prev_link.get('href')
    # Get the prev button's url
    prev_link = soup.select('#strip a')[0]
    url = 'http://bunny-comic.com/' + prev_link.get('href')

print('Done')