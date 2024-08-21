from datetime import datetime
from flask import current_app as app
from ..utils import date as date_utils
class ContractsRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("contracts")

    def get_last_inserted_contract_code(self):
        last_inserted_contract_code = self.collection.find_one(sort=[('_id', -1)], projection={'code': 1, '_id': 0})
        return last_inserted_contract_code['code'] if last_inserted_contract_code else None
    
    def get_last_id(self):
        last_inserted_contract_id = self.collection.find_one(sort=[('_id', -1)], projection={'_id': 1})
        return last_inserted_contract_id['_id'] if last_inserted_contract_id else None

    def insert_one(self, contract_dict, mdb_session):
        result = self.collection.insert_one(contract_dict, session = mdb_session)
        return result.inserted_id
    
    def find_by_code(self, code, only_id = None):
        if only_id:
            return self.collection.find_one({"code": code}, projection={'_id': 1})
        return self.collection.find_one({"code": code})
    
    def find_many_by_type(self, type, only_ids = False):
        if only_ids:
            contracts = self.collection.find({"type": type}, projection={'_id': 1})
            return list(contracts)
        return list(self.collection.find({"type": type}))
    
    
    def find_many_by_first_implantation_payment_date_year(self, year):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        contracts = self.collection.find({
        'first_implantation_payment_date': {
            '$gte': start_date,
            '$lt': end_date
            },
        })
        return list(contracts)
    
    def find_many_by_signed_at_year(self, year):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        
        contracts = self.collection.find({
        'signed_at': {
            '$gte': start_date,
            '$lt': end_date
            },
        })
        return list(contracts)
    
    def get_new_clients_count_by_month(self, date):
        converted_date = date_utils.convert_date_utc(date)
        start_date = datetime(converted_date.year, converted_date.month, 1)
        end_date = datetime(converted_date.year, converted_date.month + 1, 1)
        contracts = self.collection.count_documents({
        'signed_at': {
            '$gte': start_date,
            '$lt': end_date
            },
        })
        return contracts


    