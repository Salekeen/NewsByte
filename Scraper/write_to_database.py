from datetime import datetime
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

import os
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(
    f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/Scratch"
)
metadata = MetaData(engine)
article_table = Table('articles', metadata, autoload=True)
connection = engine.connect()


def write_to_database(headlines, article_bodies, urls):
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
