import bs4
import requests
import os

os.makedirs('comic', exist_ok=True)
url = r'http://xkcd.com/'


def get_prev_link(page_html):
    link = page_html.select('a[rel="prev"]')[0]
    # print('previous link {}'.format(prev_link))
    return 'http://xkcd.com' + link.get('href')


while not url.endswith('#'):
    '''
    Download the page.

    Find the URL of the comic image.

    Download the image.

    Save the image to ./comic.

    Get the Prev button's url.
     '''
    # Download the page
    print('Downloading the page {}...'.format(url))
    res = requests.get(url=url)
    res.raise_for_status()

    # url of comic image
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    comic_ele = soup.select('#comic img')
    # print(comic_ele)
    if not comic_ele:
        print("Image not found...")
        url = get_prev_link(soup)
        continue

    else:
        try:
            comic_url = 'http:' + comic_ele[0].get('src')
            print('Downloading image {} ...'.format(comic_url))
            image_res = requests.get(comic_url)
            image_res.raise_for_status()
        except requests.exceptions.MissingSchema:

            # skip those aren't images
            url = get_prev_link(soup)
            continue

        # saving the image
        image_file = open(os.path.join('comic', os.path.basename(comic_url)), 'wb')
        for chunk in image_res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()

        # prev button's url
        url = get_prev_link(soup)

print('Downloading completed...')












