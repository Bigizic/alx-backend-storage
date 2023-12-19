#!/usr/bin/env python3
"""
a function that returns all students sorted by average score
@param (mongo_collection): <object pymongo>

Return: returns all students sorted by average score
"""


def top_students(mongo_collection):
    """Implementation
    """
    pipeline = [
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'averageScore': {
                    '$avg': {
                        '$avg': '$topics.score',
                    },
                },
                'topics': 1,
            },
        },
        {
            '$sort': {'averageScore': -1},
        },
    ]
    return mongo_collection.aggregate(pipeline)
