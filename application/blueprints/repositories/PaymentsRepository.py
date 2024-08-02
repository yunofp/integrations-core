from flask import current_app as app

class PaymentsRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("payments")

    def get_last_id(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)], projection={'_id': 1})
        return last_inserted_document.get('_id')
    
    def insert_one(self, payment_dict, mdb_session):
        result = self.collection.insert_one(payment_dict, session = mdb_session)
        return result.inserted_id
    