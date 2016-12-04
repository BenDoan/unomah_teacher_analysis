#!/usr/bin/env python2

import datetime
import json
import logging
import re
import string
import time
import pickle

import requests

from BeautifulSoup import BeautifulSoup

from util import Teacher, TeacherRating

logging.basicConfig(level=logging.INFO)

BASE_URL = "http://www.unomaha.edu/registrar/students/before-you-enroll/class-search/"

TEACHER_LISTING_URL = "http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&rows=20000&callback=noCB&q=*%3{}*+AND+schoolid_s%3A1307&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="
TEACHER_PAGE_URL = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid={}&page={}"


def find_teachers():
    teachers = set()
    for letter in list(string.ascii_lowercase):
        url = TEACHER_LISTING_URL.format(letter)
        logging.info("Requesting %s", url)
        r = requests.get(url)
        time.sleep(.5)
        if r.status_code == 200:
            # format is noCB({...json...});
            try:
                rmp_resp = json.loads(r.text[5:-2])['response'] # extract out json
            except:
                continue
            num_found = rmp_resp['numFound']

            for teacher in rmp_resp['docs']:
                try:
                    t = Teacher(teacher['teacherfirstname_t'], teacher['teacherlastname_t'],
                                teacher['total_number_of_ratings_i'],
                                teacher['averageratingscore_rf'], teacher['pk_id'])
                    teachers.add(t)
                except KeyError:
                    # invalid teacher
                    continue
    logging.info("Found %s teachers total", len(teachers))
    return teachers

def find_teacher_ratings(teacher):
    ratings = set()
    for page in range(100):
        url = TEACHER_PAGE_URL.format(teacher.rmp_id, page)
        logging.info("Requesting %s", url)
        r = requests.get(url)
        time.sleep(.5)

        j = r.json()
        if j.get('remaining', 0) <= 0:
            break

        for i in j.get('ratings', {}):
            rating = TeacherRating(i.get('rClass'), i.get('rComments'), i.get('rDate'),
                                   i.get('rEasy'), i.get('rClarity'), i.get('rHelpful'),
                                   i.get('rOverall'), i.get('quality'), i.get('rWouldTakeAgain'),
                                   i.get('teacherGrade'), tuple(i.get('teacherRatingTags')))
            ratings.add(rating)
    return ratings



def _main():
    out_dict = []

    teachers = find_teachers()
    for teacher in teachers:
        ratings = find_teacher_ratings(teacher)
        out_dict.append((teacher, ratings))

    with open("ratings.pickle", "w+") as f:
        pickle.dump(out_dict, f)



if __name__ == "__main__":
    _main()


