#!/usr/bin/python3

from utils.db import DBClient

db_client = DBClient()

db_client.connect_to_collection("events")

result = db_client.get_all_documents()
print(result)
