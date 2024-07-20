from flask import current_app as app

class profileRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("profile")
    
    def insert_profile_data(self, profile_dict, mdb_session):
        profile_document = self.collection.insert_one(profile_dict, session = mdb_session)
        return profile_document
        
    
    def insert_profile_document(self, profile_dict):
        with app.dbClient.start_session() as session:
            with session.start_transaction():
                try:
                    document = self.insert_profile_data(profile_dict, session)
                    return document
                except Exception as e:
                      raise  # Rethrow the exception to trigger rollback
    
    def cod_already_exists(self, cod):
        if self.collection.find_one({"cpfcnpj": cod}) is not None:
            return True
        
        return False
    
    def get_last_profile_document_id(self, cod):
        return self.collection.find_one({"cod": cod}, {"_id": 1})["_id"]