from flask import current_app as app

class EntriesRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("entries")

    def get_last_id(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)], projection={'_id': 1})
        return last_inserted_document.get('_id')
    
    def insert_one(self, entry_dict, mdb_session):
        self.collection.insert_one(entry_dict, session = mdb_session)
    
