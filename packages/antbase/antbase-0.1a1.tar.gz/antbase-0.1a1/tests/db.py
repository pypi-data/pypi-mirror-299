from __future__ import annotations

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antbase.base.db import Db

c_1 = Db.test_c_1
c_2 = ('test','c_2')

# Insert document
docs = [
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0010", 'n': 100},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0011", 'n': 200},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0012", 'n': 300},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0013", 'n': 400},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0014", 'n': 500},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0015", 'n': 600},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0016", 'n': 700},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0017", 'n': 800},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0018", 'n': 900},
    {'db': c_1[0], 'collection': c_1[1], 'type': "skoOrder", 'id': "p0019", 'n': 1000}]

doc_2 = {'db': c_2[0], 'collection': c_2[1], 'type': "skoOrder", 'id': "p0010", 'n': 100}
print(f"Document to insert: {docs}")
print(f"Document to insert: {doc_2}")

col_1 = Db(c_1)
col_2 = Db(c_2)

id1 = col_1.insert(docs)
id2 = col_1.insert_one(doc_2)
if id1: print(f"Inserted documents ID1: {id1}")
if id2: print(f"Inserted document ID2: {id2}")

# Find document by ID
filter_a = {'id': "p0010"}
filter_b = {'type': "skoOrder"}
print(f"Filter A: {filter_a}")
doc_a = col_1.find_one(filter_a)
if doc_a: print(f"Document found (A): {doc_a}")

# Find multiple documents with limit 5
doc_b = col_1.find(filter_b, limit=5)
if doc_b:
    print(f"Documents found (B): {doc_b}")
    print(f"Number of documents found (B): {len(doc_b)}")

# Find by ID using MongoDB ObjectID
filter = {'_id': id2}
print(f"Filter with ObjectID: {filter}")

# Uncomment the following line to delete the document if necessary
# ndel = Db.delete_one(db, collection, filter)
# if ndel:
#     print(f"Number of documents deleted: {ndel}")

# Find a different document by ID
doc_c = col_1.find(filter)
doc_d = col_1.find({'id': "p0015"})
if doc_c:
    print(f"Documents found (C): {doc_c}")
    print(f"Number of documents found (C): {len(doc_c)}")

if doc_d:
    print(f"Documents found (D): {doc_d}")
    print(f"Number of documents found (D): {len(doc_d)}")

# Update document
update_result = col_1.update({'id': "p0010"}, {'$set': {'status': "open"}})
if update_result:
    print(f"Update result: {update_result}")
