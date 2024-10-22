#!/usr/bin/env python3
"""
*Top students
"""


def top_students(mongo_collection):
    """
    a Python function that returns all students sorted by average score:
        Prototype: def top_students(mongo_collection):
        mongo_collection will be the pymongo collection object
        The top must be ordered
        The average score must be part of each item returns with key = averageScore
    """
    students = mongo_collection.find()
    student_list = []
    
    for student in students:
        average_score = sum(topic['score'] for topic in student['topics']) / len(student['topics'])
        student_list.append(
            {
                **student,
                'averageScore': average_score
            }
        )

    sorted_students = sorted(student_list, key=lambda x: x['averageScore'], reverse=True)
    return sorted_students