from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger(__name__)

engine = create_engine(settings.postgres_url, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_db():
    db = SessionLocal()
    log.info("\nDB Session created...")
    try:
        yield db
    finally:
        db.close()