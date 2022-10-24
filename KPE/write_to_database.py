from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import and_
from sqlalchemy import insert
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import IntegrityError

import os
from dotenv import load_dotenv
load_dotenv()


def write_to_database(kpe):
    # Establishing Setup
    engine = create_engine(
        f"postgresql+psycopg2://{os.environ['dbUSERNAME']}:{os.environ['dbPASSWORD']}@localhost:5432/Scratch"
    )
    metadata = MetaData(engine)
    keyphrase7 = Table('keyphrase7', metadata, autoload=True)
    connection = engine.connect()

    ins = insert(keyphrase7).values(
        date=datetime.today(),
        kp=kpe,
    )
    connection.execute(ins)
    connection.close()

    