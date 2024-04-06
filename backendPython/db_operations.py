from pymongo import MongoClient

class DBOperations:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['fraud_detection']
        self.collection = self.db['fraudData']

    def get_all_transactions(self):
        return list(self.collection.find({}, {'_id': 0}))

    def insert_transaction(self, transaction):
        self.collection.insert_one(transaction)
