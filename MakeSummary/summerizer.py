# importing all the dependencies

from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from load_data import get_last_n_days_data
from write_to_database import write_to_database

from prefect import task, flow
from prefect.task_runners import SequentialTaskRunner


@task(
    retries=2,
    retry_delay_seconds=60
)
def get_data():
    """
    It takes the last n days of data from the database and returns the article_id and article_body as
    two separate lists
    
    Returns:
      article_id and article_body
    """

    data = get_last_n_days_data(n=1)
    print(data.shape)
    article_id = data['article_id']
    article_body = data['article_body']
    return article_id, article_body


@task(
    retries=2,
    retry_delay_seconds=60
)
def make_summery(article_id, article_body):
    """
    It takes in a list of article_ids and a list of article_bodies and returns a list of article_ids and
    a list of summeries.
    
    Args:
      article_id: The id of the article
      article_body: The text of the article
    
    Returns:
      A tuple of article_id and summeries
    """
    
    stemmer = Stemmer("english")
    summerizer = Summarizer(stemmer)
    summeries = []
    for article in article_body:
        summery = ""
        parser = PlaintextParser.from_string(article, Tokenizer("english"))
        for sentence in summerizer(parser.document, 2):
            summery += f"{sentence}\n"
        summeries.append(summery)
    return article_id, summeries


@flow(
    name="Summerizer Flow",
    task_runner=SequentialTaskRunner()
)
def summerizer_flow():
    """
    It gets data, makes a summary, and writes it to a database
    """
    
    article_id, article_body = get_data()
    article_id, summeries = make_summery(article_id, article_body)
    write_to_database(article_id, summeries)


if __name__ == "__main__":
    summerizer_flow()
