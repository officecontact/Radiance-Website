import os
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

URL_FILE = "images_urls.txt"
OUTPUT_FOLDER = "images"
THREADS = 30

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def clean_url(url):
    return url.strip().rstrip("'").rstrip("]")

def get_filename(url):

    parsed = urlparse(url)
    path_parts = parsed.path.split("/")

    # last two parts create unique filename
    if len(path_parts) >= 3:
        name = path_parts[-2] + "_" + path_parts[-1]
    else:
        name = path_parts[-1]

    return name

def download(url):

    url = clean_url(url)
    filename = get_filename(url)
    path = os.path.join(OUTPUT_FOLDER, filename)

    if os.path.exists(path):
        print("Skipped:", filename)
        return

    try:

        r = requests.get(url, headers=HEADERS, timeout=20)

        if r.status_code == 200:

            with open(path, "wb") as f:
                f.write(r.content)

            print("Downloaded:", filename)

        else:
            print("Failed:", r.status_code, url)

    except Exception as e:
        print("Error:", url, e)


def main():

    with open(URL_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]

    print("Total URLs:", len(urls))

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(download, urls)


if __name__ == "__main__":
    main()