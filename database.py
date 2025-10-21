from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg2://postgres:admin123@localhost:5432/Khushi"
engine = create_engine(db_url)
session =  sessionmaker(autocommit = False,autoflush=True,bind=engine)