from flask import current_app as app

class ProcessedRequestsRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.processed_requests
     
    def getLastProcessedRequest(self):
        last_processed_request = self.collection.find().sort('requestId', -1).limit(1)
        last_processed_request = list(last_processed_request)
        return last_processed_request[0] if last_processed_request else None
    
    def insertOne(self, data):
        result = self.collection.insert_one(data)
        return result
        