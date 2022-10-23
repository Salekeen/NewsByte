from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, create_engine)
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(
    f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/ScrapedData"
)

metadata = MetaData()

summeries = Table(
    'summeries',metadata,
    Column('summery_id',Integer(),primary_key=True,autoincrement=True),
    Column('url',String()),
    Column('headline',String()),
    Column('summery',String()),
    Column('date_published',DateTime())
)
metadata.create_all(engine)