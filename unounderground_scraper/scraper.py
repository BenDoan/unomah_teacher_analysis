#!/usr/bin/env python2

import datetime
import json
import logging
import re
import string
import time
import pickle

import requests

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

TOC_URL = "http://www.unounderground.com/TeacherDisc/TeacherDiscussion_tocf.htm"
REVIEW_URL = "http://www.unounderground.com/TeacherDiscussion/{}.htm"

def get_reviews():
    r = requests.get(TOC_URL)
    toc_soup = BeautifulSoup(r.text, 'html.parser')

    review_links = toc_soup.find_all("dt")

    reviews = {}
    for i, link in enumerate(review_links):
        try:
            review_number = link.find('a').attrs['name']

            url = REVIEW_URL.format(review_number)
            logging.info("Requesting %s (%s/%s)", url, i, len(review_links))
            r = requests.get(url)
            time.sleep(.2)
            review_soup = BeautifulSoup(r.text, 'html.parser')

            name = review_soup.find("h2").text
            if name == "Pick a Teacher!":
                continue

            text = review_soup.find_all("p")

            meta = text[2].text
            improvement = text[3].text
            comments = text[4].text

            if name not in reviews:
                reviews[name] = []
            reviews[name].append({
                "improvement": improvement,
                "comments": comments,
                "meta": meta
            })
        except:
            logging.exception("Failed to parse page")
            continue

    for r in reviews:
        r = list(set(r))

    return reviews

def _main():
    out_dict = []

    reviews = get_reviews()

    with open("unou_reviews.pickle", "w+") as f:
        pickle.dump(reviews, f)



if __name__ == "__main__":
    _main()


