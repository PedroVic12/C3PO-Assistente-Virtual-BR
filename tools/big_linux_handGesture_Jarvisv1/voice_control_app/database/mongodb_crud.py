from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def create(self, collection: str, data: Dict) -> str:
        pass

    @abstractmethod
    def read(self, collection: str, query: Dict) -> List[Dict]:
        pass

    @abstractmethod
    def update(self, collection: str, query: Dict, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete(self, collection: str, query: Dict) -> bool:
        pass

class MongoDBCRUD(DatabaseInterface):
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.connect()

    def connect(self) -> None:
        try:
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('MONGODB_DB', 'voice_control_app')]
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

    def disconnect(self) -> None:
        if self.client:
            self.client.close()

    def _get_collection(self, collection_name: str) -> Collection:
        if not self.db:
            raise ConnectionError("Database not connected")
        return self.db[collection_name]

    def create(self, collection: str, data: Dict) -> str:
        try:
            result = self._get_collection(collection).insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Failed to create document: {str(e)}")

    def read(self, collection: str, query: Dict) -> List[Dict]:
        try:
            return list(self._get_collection(collection).find(query))
        except Exception as e:
            raise Exception(f"Failed to read documents: {str(e)}")

    def update(self, collection: str, query: Dict, data: Dict) -> bool:
        try:
            result = self._get_collection(collection).update_one(query, {"$set": data})
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update document: {str(e)}")

    def delete(self, collection: str, query: Dict) -> bool:
        try:
            result = self._get_collection(collection).delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Failed to delete document: {str(e)}")

    def __del__(self):
        self.disconnect()
