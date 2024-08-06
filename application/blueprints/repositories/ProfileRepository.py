from flask import current_app as app

class ProfileRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("profiles")
    
    def insert_one(self, profile_dict, mdb_session):
        profile_document = self.collection.insert_one(profile_dict, session = mdb_session)
        return profile_document
    
    def get_last_profile_document_id(self, cod):
        return self.collection.find_one({"cod": cod}, {"_id": 1})["_id"]