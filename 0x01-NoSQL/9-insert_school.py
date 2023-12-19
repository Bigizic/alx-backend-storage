#!/usr/bin/env python3
"""function that inserts a new document in a collection based on kwargs

@param (mongo_collection): <object pymongo>
@param (**kwargs): <keyword arguments>

Return: new attribute _id
"""


def insert_school(mongo_collection, **kwargs):
    """Implementation
    """
    if kwargs:
        result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
