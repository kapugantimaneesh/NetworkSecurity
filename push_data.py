import os
import json
import sys

from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
print(MONGO_DB_URI)

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_tomongo(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URI,
                tlsCAFile=ca
            )

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "network_data/phisingData.csv"
    DATABASE = "Maneesh"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

    record = networkobj.csv_to_json_convertor(FILE_PATH)

    print(f"Total Records Found: {len(record)}")

    no_of_records = networkobj.insert_data_tomongo(
        records=record,
        database=DATABASE,
        collection=COLLECTION
    )

    print(f"{no_of_records} records inserted successfully.")