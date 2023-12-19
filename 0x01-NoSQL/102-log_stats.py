#!/usr/bin/env python3
""" Improved 12-log_stats.py
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
    print("IPs:")

    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}},
        {"$sort": {"totalRequests": -1}},
        {"$limit": 10}
    ])

    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['totalRequests']}")


if __name__ == '__main__':
    nginx_stats()
