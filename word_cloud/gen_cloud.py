#!/usr/bin/env python2
import pickle
import re
import sys

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from util import Teacher, TeacherRating

common_words = [
    "know", "class" "lot" "the", "teaches", "teaches",
    "help", "stuff", "office", "ll", "teacher", "people",
    "lot", "ask", "talking", "willing", "don", "class",
    "everything", "material", "test", "goes", "seems", "causes",
    "also", "text", "graded", "everyone", "time", "lecture", "lectures",
    "outside", "little", "much", "gives", "well", "always", "question", "make",
    "take", "assignment", "professor", "course", "grade", "will", "subject", "took"
    "semester", "took", "one", "two", "three", "assignments", "every", "uno", "semester",
    "final", "pretty", "quot", "going", "wants", "student", "really", "lots", "questions",
    "quizzes", "tests", "makes", "definitely", "ok", "go", "teaching", "students", "ever",
    "anything", "guy", "believes", "since", "use", "feel", "point", "thing", "even", "things"
]


def get_rmp_comments(teachers, teacher_lastname):

    for teacher, ratings in teachers:
        if teacher.lastname == teacher_lastname:
            comments = [x.comments for x in ratings]
            return " ".join(comments)

def get_all_rmp(teachers):
    text = []
    for teacher, ratings in teachers:
        text.append(" ".join([x.comments for x in ratings]))
    return " ".join(text)

def get_unou_comments(reviews, teacher_lastname):
    for name, t_reviews in reviews.items():
        if teacher_lastname in name:
            return " ".join([x['improvement'] + " " + x['comments'] for x in t_reviews])


def clean_text(orig_text):
    text = orig_text.lower()
    text = re.sub("[^A-Za-z ']", " ", text)
    text = text.split(" ")
    for word in common_words:
        text = filter(lambda x: x.strip() != word, text)

    return " ".join(text)

def plot_cloud(text):
    wordcloud = WordCloud(width=1000, height=600).generate(text)

    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def _main():
    with open("rmp_ratings.pickle", "rb") as f:
        teachers = pickle.load(f)
    with open("unou_reviews.pickle", "rb") as f:
        unou_reviews = pickle.load(f)

    text = get_rmp_comments(teachers, sys.argv[1])
    # text = get_unou_comments(unou_reviews, sys.argv[1])
    # text = get_all_rmp(teachers)
    plot_cloud(clean_text(text))

if __name__ == '__main__':
    _main()
