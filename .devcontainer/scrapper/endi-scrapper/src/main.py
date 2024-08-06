import time
import logging
from datetime import datetime, timedelta
from helpers.manager_articles import current_articles, Article
from helpers.manager_db import DBManager

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s :: %(module)s -> %(message)s')
logger = logging.getLogger(__name__)

print("")
logger.info("****************    SCRAPPER WORKING    ****************")

while True:
    # Fetch current articles
    logger.info("Fetching current articles")

    articles_result_set = current_articles()

    for article_tag in articles_result_set:
        print("")
        logger.info("Initializing Article and Database objects")

        # Initialize article manager
        article = Article(tag = article_tag)
        # Initialize database manager
        dbconsultor = DBManager()

        logger.info("Calculating article hash and consulting database")

        if dbconsultor.check_hash(article.get_hash()):
            logger.info(f"Article hash already contained in database")
        else:
            logger.info("!!!!!!!!!!!!!!    NEW ARTICLE FOUND    !!!!!!!!!!!!!!")
            article_data_dict = article.construct_data_dict()
            dbconsultor.write_in_tables(article_data_dict)

    print("")
    logger.info("****************    ENDING SCAN    ****************")
    logger.info("Waiting 30 mins for next scan")
    next_scan_time = (datetime.now() - timedelta(hours=5)) + timedelta(minutes=30)
    logger.info(f"Next scan at {next_scan_time}")
    time.sleep(1800)
