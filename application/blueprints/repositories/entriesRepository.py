from datetime import datetime
from flask import current_app as app
import pandas as pd

class EntriesRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("entries")

    def get_last_id(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)], projection={'_id': 1})
        return last_inserted_document.get('_id')
    
    def insert_one(self, entry_dict, mdb_session):
        self.collection.insert_one(entry_dict, session = mdb_session)
    
    def insert_many(self, entries, mdb_session):
        self.collection.insert_many(entries, session = mdb_session)
        
    def find_many_by_year_by_contracts_ids(self, year, contracts_ids):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        entries = self.collection.find({
        'payment_date': {
            '$gte': start_date,
            '$lt': end_date
        },
        'contract_id': {
            '$in': contracts_ids
        }})
        return list(entries)
    
