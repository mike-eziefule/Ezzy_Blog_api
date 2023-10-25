#dependencies injection
from typing import Generator
from database.database import sessionLocal

class injection:
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = sessionLocal()
            yield db
        finally:
            db.close()