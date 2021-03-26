from src.config import config
from src.database import Database

database = Database(config)
database.migrate()
