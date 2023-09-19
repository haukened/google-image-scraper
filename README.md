# <span style="font-weight: bold; font-size: 1.25em;"><span style="color: blue;">G</span><span style="color: red;">o</span><span style="color: gold;">o</span><span style="color: blue;">g</span><span style="color: green;">l</span><span style="color: red;">e</span></span> Image Scraper

<div style="display:flex; flex-direction: row; gap: 5em; justify-content: space-between;">
    <p>A python script for web scraping, to collect images for machine learning model training.</p>
    <img alt="a space python ready to steal your images" style="" src="README.png" width="100px">
</div>

## What is this?
In experimenting with some image classification machine learning, I realized that for some nice industrial things the images that I was needing to work with were very poorly represented in available public data sets.  

Obviously the solution was to contact every single customer and ask them to take hundreds of pictures 
of things from every angle **right?**

I created this script to kick-start some of those machine learning tasks, and realized it could really be useful for everyone else too.

## Is this legal where I live/work/etc.. ?

(**THIS IS NOT LEGAL ADVICE - I AM NOT A LAWYER**)

tl;dr - Probably not.  

Legalities of things vary widely based on your geographic location, and where your code is deployed.  If you're in Europe using a virtual machine in the United States for a project that will be deployed in China, I can't really help you on the legality of that, or what law applies.

In general, however, unless license is explicitly granted for use of images, the copyright of those images belongs to the photographer / publisher.  As such, re-distribution and use of those images may be restricted in some manner.  Its up to you to comply with the law, and this software is being made available as a learning tool, without warranty.

## How does <span style="font-weight: bold; font-size: 1.25em;"><span style="color: blue;">G</span><span style="color: red;">o</span><span style="color: gold;">o</span><span style="color: blue;">g</span><span style="color: green;">l</span><span style="color: red;">e</span></span> feel about this?

To quote the [Google Terms of Service](https://policies.google.com/terms):

>Google reserves the right to suspend or terminate your access to the services or delete your Google Account if any of these things happen:
>
>- you materially or repeatedly breach these terms, [service-specific additional terms or policies](https://policies.google.com/terms/service-specific?hl=en-US)
>- we’re required to do so to comply with a legal requirement or a court order
>- your conduct causes harm or liability to a user, third party, or Google — for example, by hacking, phishing, harassing, spamming, misleading others, or <mark>scraping content that doesn’t belong to you</mark>

So that being said, not all scraping is a ToS violation. People surf Google Images and download content for their own personal use every day, the semantics involve how much, how fast, and improtantly _for what purpose_.  Take care to keep to a resonable number of images, that you intend to use for the proper purposes.

## Quick Start

1. Clone this repository somewhere on your machine

    `git clone https://github.com/haukened/google-image-scraper`

1. Move into the cloned directory

    `cd google-image-scraper`

1. Create a python [virtual environment](https://docs.python.org/3/library/venv.html) (Optional, however keeps dependencies clean)

    `python3 -m venv .venv`

    `source ./.venv/bin/activate`

1. Install dependencies

    `pip install -r requirements.txt`

1. Run the scraper

    `./scrape.py a bear riding a tricycle`

1. Explore the options

    `./scrape.py -h`

    ```
    usage: scrape.py [-h] [-s] [-v] [-n NUMBER] [-o OUTPUT_DIRECTORY] [query ...]

    Downloads images from Google image search

    positional arguments:
    query                 the search query for images. aka "What you would type into google"

    options:
    -h, --help            show this help message and exit
    -s, --show-browser    show the browser during downloading
    -v, --verbose         show debug information
    -n NUMBER, --number NUMBER
                            number of images to download
    -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            the path to store downloaded images

    Created by @haukened | Buy me a beer: https://beer.hauken.us
    ```

## Examples

Show the browser during scraping, add the `-s` flag
- `./scrape.py -s -n 500 jimmy kimmel laughing`

Store the images somewhere else
- `./scrape.py -n 1000 -o /home/<you>/datasets/bears/ the greatest threat to america`