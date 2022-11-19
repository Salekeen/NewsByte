from datetime import datetime
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

import os
from dotenv import load_dotenv
load_dotenv()

from prefect import task


engine = create_engine(
    f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/Scratch"
)
metadata = MetaData(engine)
article_table = Table('articles', metadata, autoload=True)
connection = engine.connect()

@task(
    retries=2,
    retry_delay_seconds=60
)
def write_to_database(headlines, article_bodies, urls):
    """
    It writes the data to the database.
    
    Args:
      headlines: a list of strings, each string is a headline
      article_bodies: list of article bodies
      urls: list of urls
    """
    
    for i in range(len(headlines)):
        try:
            ins = insert(article_table).values(
                url=urls[i],
                headline=headlines[i],
                article_body=article_bodies[i],
                date_published=datetime.today(),
            )
            connection.execute(ins)
        except IntegrityError:
            pass
    connection.close()
