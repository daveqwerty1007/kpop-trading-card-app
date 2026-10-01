import os
import sys
import requests

# Never commit this key; export it before running the script.
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
UNSPLASH_URL = 'https://api.unsplash.com/photos/random'
UNSPLASH_LIMIT = 50

def fetch_unsplash_image_urls():
    image_urls = []
    for _ in range(UNSPLASH_LIMIT):
        response = requests.get(UNSPLASH_URL, params={'client_id': UNSPLASH_ACCESS_KEY})
        if response.status_code == 200:
            try:
                data = response.json()
                image_urls.append(data['urls']['small'])
            except ValueError:
                print('Failed to decode JSON response:')
                print(response.text)
        else:
            print(f'Failed to fetch image from Unsplash (status code: {response.status_code}).')
            print(response.text)
    return image_urls

def save_image_urls(image_urls, filename='image_urls.txt'):
    with open(filename, 'w') as file:
        for url in image_urls:
            file.write(url + '\n')

def main():
    if not UNSPLASH_ACCESS_KEY:
        sys.exit('Set UNSPLASH_ACCESS_KEY to your Unsplash API access key first.')
    image_urls = fetch_unsplash_image_urls()
    save_image_urls(image_urls)
    print(f'Successfully fetched and saved {len(image_urls)} image URLs.')

if __name__ == "__main__":
    main()
