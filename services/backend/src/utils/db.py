from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.utils.config import config

engine = create_engine(config.DATABASE_URL,  connect_args=config.SSL_PARAMS, pool_pre_ping=True)
session_not_thread_safe = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is going to create a scoped thread safe database session
# Source: https://docs.sqlalchemy.org/en/20/orm/contextual.html
SessionLocal = scoped_session(session_factory=session_not_thread_safe)
