#!/usr/bin/env python3

import argparse
import base64
import hashlib
import io
import os
import pathlib
import requests
import sys
import urllib.parse

from enum import Enum
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

class Level(Enum):
    ERROR = 'ERROR'
    WARN = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'

def print_log(level: Level, message:str, e:Exception=None) -> None:
    if args.verbose:
        if e is not None:
            print("{level}: {message} - {exception}".format(level=level, message=message, exception=e))
        else:
            print("{level}: {message}".format(level=level, message=message))

def fetch_images(query:str, max:int, wd:webdriver, path:str="photos", sleep_between_interactions:float=1.0):
    # URL encode the query
    encoded_query = urllib.parse.quote(query)
    # for folder name, replace spaces with underscores
    folder_name = os.path.join(path, query.replace(" ", "_"))
    # build the query
    search_url = "https://www.google.com/search?tbm=isch&q={0}".format(encoded_query)
    # load the page
    wd.get(search_url)
    image_count = 0
    results_start = 0

    pbar = tqdm(desc="Fetching images", total=max)
    # get images
    while image_count < max:
        # get all image thumbnail results
        thumbnails = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        num_thumbs = len(thumbnails)

        # get higher res versions
        for img in thumbnails[results_start:num_thumbs]:
            # sroll to the thumbnail
            try:
                wd.execute_script("arguments[0].scrollIntoView(true);", img)
            except Exception as e:
                print_log(Level.WARN, "unable to scroll to element", e)
                continue
            # try to click every thumbnail so we can get the real image behind it
            try:
                # click the image. What happens here is a low-res version is preloaded by google while we wait for the actual fetch to happen for the full-res source
                img.click()
                # wait for the full resolution element to load
                element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.iPVvYb')))
                # grab its source element
                src = element.get_attribute('src')
                # if its valid save it
                if 'http' in src:
                    contents = get_image_contents(src)
                    if contents:
                        ok = persist_image(contents, folder_name)
                        if ok:
                            image_count += 1
                            pbar.update(1)
                else:
                    print_log(Level.INFO, "image did not have a src element")
                # quit when we have enough images
                if image_count >= max:
                    pbar.close()
                    print(f"Found: {image_count} images, done!")
                    return
            except Exception as e:
                print_log(Level.WARN, "unable to process current image", e)
                continue                 

        # then store the current part to continue
        results_start = image_count

def get_image_contents(url:str) -> bytes:
    try:
        image_content = requests.get(url).content
        return image_content
    except Exception as e:
        print_log(Level.ERROR, "unable to get image contents", e)
        return ""

def persist_image(image_content:bytes, path:str) -> bool:
    try: 
        image_src = io.BytesIO(image_content)
        image = Image.open(image_src).convert("RGB")
        file_path = os.path.join(path,hashlib.sha1(image_content).hexdigest() + '.jpg')
        p = pathlib.Path(path)
        p.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print_log(Level.INFO, "saved image {}".format(file_path))
        return True
    except Exception as e:
        print_log(Level.ERROR, "unable to save image {}".format(file_path), e)
        return False

def deocde_b64_image(src:str) -> str:
    b = bytes(src, 'ascii')
    start = b.find(b'/9')
    if start > 0:
        return base64.b64decode(b[start:])
    else:
        return base64.b64decode(b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="scrape.py",
        description="Downloads images from Google image search",
        epilog="Created by @haukened | Buy me a beer: https://beer.hauken.us",
    )
    parser.add_argument('-s', '--show-browser', action='store_true', help="show the browser during downloading")
    parser.add_argument('-v', '--verbose', action='store_true', help="show debug information")
    parser.add_argument('-n', '--number', default=5, type=int, help="number of images to download")
    parser.add_argument('-o', '--output-directory', type=pathlib.Path, default="images", help="the path to store downloaded images")
    parser.add_argument("query", nargs='*', type=str, help="the search query for images. aka \"What you would type into google\"")
    args, trash = parser.parse_known_args()
    if trash != []:
        print("unknown options {}".format(trash), file=sys.stderr)
        parser.print_help(sys.stderr)
        raise SystemExit(1)
    if len(args.query) == 0:
        print("no query supplied", file=sys.stderr)
        parser.print_help(sys.stderr)
        raise SystemExit(2)
    query = " ".join(args.query)
    chrome_options = Options()
    if not args.show_browser:
        chrome_options.add_argument('--headless')
    wd = webdriver.Chrome(options=chrome_options)
    fetch_images(query, args.number, wd, args.output_directory)
    wd.quit()