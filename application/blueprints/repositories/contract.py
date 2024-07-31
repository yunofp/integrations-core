from flask import current_app as app

class contractRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("contracts")

    def get_last_inserted_contract_code(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)])
        return last_inserted_document.get('cod')
    
    def get_last_id(self):
        last_inserted_document = self.collection.find_one(sort=[('_id', -1)])
        return last_inserted_document.get('_id')

    def insert_contract_data(self, contract_dict, mdb_session):
        self.collection.insert_one(contract_dict, session = mdb_session)

    def cod_already_exists(self, cod):
        if self.collection.find_one({"cod": cod}) is not None:
            return True
        
        return False

    def insert_contract_document(self, contract_dict):
        with app.dbClient.start_session() as session:
            with session.start_transaction():
                try:
                    self.insert_contract_data(contract_dict, session)
                except Exception as e:
                      raise  # Rethrow the exception to trigger rollback


    