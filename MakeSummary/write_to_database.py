from sqlite3 import IntegrityError
from sqlalchemy import and_
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

import os
from dotenv import load_dotenv
load_dotenv()


def write_to_database(article_id, summeries):
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
