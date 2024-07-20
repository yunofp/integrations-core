from flask import current_app as app

class extractRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("extract")

    def get_last_id(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)])
        return last_inserted_document.get('_id')
    
    def insert_extract_data(self, extract_dict, mdb_session):
        self.collection.insert_one(extract_dict, session = mdb_session)
    
    def insert_extract_document(self, extract_dict):
        with app.dbClient.start_session() as session:
            with session.start_transaction():
                try:
                    self.insert_extract_data(extract_dict, session)
                except Exception as e:
                      raise  # Rethrow the exception to trigger rollback