from collections import namedtuple

Teacher = namedtuple('Teacher', ['firstname', 'lastname', 'total_ratings',
                                 'average_score', 'rmp_id'])
TeacherRating = namedtuple("TeacherRating", ['course', 'comments', 'date', 'easy_rating',
                                               'clarity_rating', 'helpful_rating',
                                               'overall_rating', 'quality_rating',
                                               'take_again', 'grade', 'tags'])

