from sqlite3 import IntegrityError
from sqlalchemy import and_
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

from prefect import task

import os
from dotenv import load_dotenv
load_dotenv()


@task(
    retries=2,
    retry_delay_seconds=60
)
def write_to_database(article_id, summeries):
    """
    It takes in two lists, one of article_ids and one of summeries, and writes them to a database.
    
    Args:
      article_id: A list of article ids
      summeries: list of strings
    """
    
    # Establishing Setup
    engine = create_engine(
        f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/Scratch"
    )
    metadata = MetaData(engine)
    summery_table = Table('summeries', metadata, autoload=True)
    connection = engine.connect()

    for i in range(len(summeries)):
        try:
            ins = insert(summery_table).values(
                article_id=int(article_id[i]),
                summery=summeries[i],
            )
            connection.execute(ins)
        except IntegrityError:
            pass
