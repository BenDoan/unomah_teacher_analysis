#!/usr/bin/env python2
import pickle
import re

from util import Teacher, TeacherRating

def median(numbers):
    return (sorted(numbers)[int(round((len(numbers) - 1) / 2.0))] + sorted(numbers)[int(round((len(numbers) - 1) // 2.0))]) / 2.0

def get_colleges_from_ratings(ratings):
    colleges = list(set([re.sub("[0-9]", "", x.course) for x in ratings]))
    if '' in colleges:
        colleges.remove('')
    return colleges

def get_teachers_by_college(teachers, college):
    ret = []
    for teacher, ratings in teachers:
        colleges = get_colleges_from_ratings(ratings)
        if college in colleges:
            ret.append((teacher, ratings))
    return ret

def _main():
    with open("ratings.pickle", "rb") as f:
        teachers = pickle.load(f)

        csci_teachers = get_teachers_by_college(teachers, "CSCI")
        cist_teachers = get_teachers_by_college(teachers, "CIST")
        isqa_teachers = get_teachers_by_college(teachers, "ISQA")
        iasc_teachers = get_teachers_by_college(teachers, "IASC")

        ist_teachers = csci_teachers + cist_teachers + isqa_teachers + iasc_teachers

        teachers_by_rating = []
        for teacher, ratings in ist_teachers:
            ratings = [x.overall_rating for x in ratings]
            avg_rating =  round(sum(ratings)/len(ratings), 2)
            teachers_by_rating.append((avg_rating, len(ratings), teacher))

        for rating, num_ratings, teacher in sorted(set(teachers_by_rating), reverse=True):
            if num_ratings > 5:
                print rating, num_ratings, teacher.firstname, teacher.lastname


if __name__ == '__main__':
    _main()
