from sqlalchemy import and_, or_, not_
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table
import os
from dotenv import load_dotenv
load_dotenv()


# Establishing Setup
engine = create_engine(
    f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/ScrapedData"
)
metadata = MetaData(engine)
all_articles = Table('all_articles', metadata, autoload=True)
top_articles = Table('top_articles', metadata, autoload=True)
connection = engine.connect()


def get_last_n_days_data(n=7):
    
    todays_date = datetime.today()
    seventh_previous_days_date = (datetime.today() - timedelta(days=n))
    s = select([all_articles]).where(
        and_(
            all_articles.c.date_published <= todays_date,
            all_articles.c.date_published >= seventh_previous_days_date
        )
    )
    rp = connection.execute(s)
    df = pd.DataFrame(rp.fetchall())
    return df
