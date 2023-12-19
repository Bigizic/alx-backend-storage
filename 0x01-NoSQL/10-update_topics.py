#!/usr/bin/env python3
""" function that changes all topics of a school document based on the name
@param (mongo_collection): <object pymongo>
@param (name): <str> school name to update
@param (topics): <list of str> list of strings

Return: modified Mongodb object
"""


def update_topics(mongo_collection, name, topics):
    """Implementation
    """
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result
