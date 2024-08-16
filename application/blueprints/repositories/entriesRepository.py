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
        
    def find_many_data_frame_by_year(self, year):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        result = self.collection.find({'created_at': {
            '$gte': start_date,
            '$lt': end_date
        }})
        
        df = pd.DataFrame(list(result))
        return df
    
