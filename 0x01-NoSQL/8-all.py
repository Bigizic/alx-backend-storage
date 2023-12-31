#!/usr/bin/env python3
"""Python scirpt that list all documents in a mongodb collection
@param (mongo_collection): <object pymongo>

Return: a list of all documents else return empty list if no documents
"""


def list_all(mongo_collection):
    """Implementation
    """
    try:
        return list(mongo_collection.find({}))
    except AttributeError as e:
        return []
