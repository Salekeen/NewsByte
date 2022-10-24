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
    f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/Scratch"
)
metadata = MetaData(engine)
articles_table = Table('articles', metadata, autoload=True)
connection = engine.connect()


def get_last_n_days_data(n=7):

    todays_date = datetime.today()
    seventh_previous_days_date = (datetime.today() - timedelta(days=n))
    s = select([articles_table]).where(
        and_(
            articles_table.c.date_published <= todays_date,
            articles_table.c.date_published >= seventh_previous_days_date
        )
    )
    rp = connection.execute(s)
    df = pd.DataFrame(rp.fetchall())
    return df
