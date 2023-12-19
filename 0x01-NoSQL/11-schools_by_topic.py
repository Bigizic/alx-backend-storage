#!/usr/bin/env python3
"""function that returns the list of school having a specific topic
@param (mongo_collection): <object pymongo>
@param (topic): <str> topic to be searched

Return: list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """Implementation
    """
    return list(mongo_collection.find({"topics": topic}))
