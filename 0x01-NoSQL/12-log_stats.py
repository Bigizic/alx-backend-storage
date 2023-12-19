#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def nginx_stats():
    """Implementation
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count
    result = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{result} status check")


if __name__ == '__main__':
    nginx_stats()
