import sys
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockDatabase:
    """
    In-memory Mock Database that simulates MongoDB collection operations.
    Enables local testing without requiring MongoDB Atlas connectivity.
    """
    def __init__(self):
        logger.warning("Initializing Mock Database (in-memory). Data will not persist across restarts!")
        self.users = []
        self.history = []

    class MockCollection:
        def __init__(self, data_list):
            self.data = data_list

        def find_one(self, query):
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    return doc
            return None

        def insert_one(self, doc):
            self.data.append(doc)
            return type('InsertedID', (object,), {'inserted_id': doc.get('_id', len(self.data))})()

        def find(self, query, sort=None):
            # Simple matching for mock history (e.g., matching username)
            results = []
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    results.append(doc)
            
            # Simple descending sort if requested by timestamp or _id
            if sort and sort[0][1] == -1:
                results.reverse()
            return results

    @property
    def users_collection(self):
        return self.MockCollection(self.users)

    @property
    def history_collection(self):
        return self.MockCollection(self.history)


# Global database interface variables
db_client = None
users_col = None
history_col = None
is_mock = True

try:
    if settings.MONGODB_URI:
        logger.info("Attempting to connect to MongoDB Atlas...")
        # 3-second connection timeout to avoid getting stuck during startup
        db_client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=3000)
        # Trigger connection check
        db_client.admin.command('ping')
        
        # Connect to mindease database
        db = db_client["mindease_db"]
        users_col = db["users"]
        history_col = db["history"]
        is_mock = False
        logger.info("Successfully connected to MongoDB Atlas!")
    else:
        logger.warning("No MONGODB_URI found in settings. Falling back to Mock Database.")
        mock_db = MockDatabase()
        users_col = mock_db.users_collection
        history_col = mock_db.history_collection
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    logger.error(f"MongoDB connection failed: {str(e)}. Falling back to Mock Database.")
    mock_db = MockDatabase()
    users_col = mock_db.users_collection
    history_col = mock_db.history_collection
except Exception as e:
    logger.error(f"Unexpected database initialization error: {str(e)}. Falling back to Mock Database.")
    mock_db = MockDatabase()
    users_col = mock_db.users_collection
    history_col = mock_db.history_collection

def get_users_collection():
    return users_col

def get_history_collection():
    return history_col

def database_status():
    return {
        "status": "connected" if not is_mock else "mock_fallback",
        "database_type": "MongoDB Atlas" if not is_mock else "In-Memory Mock Database"
    }
