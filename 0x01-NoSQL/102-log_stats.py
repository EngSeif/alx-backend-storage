#!/usr/bin/env python3
"""
*Log stats - new version
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    nginx_collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    all_nginx_rec = list(nginx_collection.find())

    # x logs where x is the number of documents in this collection
    print(f"{len(all_nginx_rec)} logs")

    # 5 lines with the number of documents with the method

    print("Methods:")
    for method in methods:
        query = nginx_collection.count_documents({"method": {"$in": [method]}})
        print(f"\tmethod {method}: {query}")

    # one line with the number of documents with:
    # method=GET
    # path=/status

    query = nginx_collection.count_documents({"$and": [
        {"method": {"$in": ["GET"]}},
        {"path": "/status"}
    ]})
    print(f"{query} status check")

    print("IPs:")
    pipline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ]
    result = nginx_collection.aggregate(pipline)
    for rec in result:
        print(f"\t{rec.get('_id')}: {rec.get('count')}")
