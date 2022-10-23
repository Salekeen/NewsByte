from sqlalchemy import and_, or_, not_
from sqlalchemy import insert
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table

from summerizer import make_summery

import os
from dotenv import load_dotenv
load_dotenv()

make_summery()


def write_to_database(summeries, urls, headlines, date_published):
    # Establishing Setup
    engine = create_engine(
        f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/ScrapedData"
    )
    metadata = MetaData(engine)
    summery_table = Table('summeries', metadata, autoload=True)
    connection = engine.connect()

    for i in range(len(summeries)):
        ins = insert(summery_table).values(
            url=urls[i],
            headline=headlines[i],
            date_published=date_published[i],
            summery=summeries[i]
        )
        connection.execute(ins)


if __name__ == "__main__":
    summeries, urls, headlines, date_published = make_summery()
    write_to_database(summeries, urls, headlines, date_published)
