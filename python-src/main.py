import time
import logging
from datetime import datetime ,timedelta
from scrapper.art_hash import get_hash
from scrapper.extract_artcls_data import current_artcls, artcl_data, artcl_content
from scrapper.location_detector import detect_location, validate_location, get_location_id
from scrapper.relevance_score_claculator import calculate_score as score
from database_manager.database_connector import dbconnection as db
from database_manager import querys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
logging.info("    ! ! ! SCRAPPER WORKING ! ! !")
# Base url
news_url= "https://www.elnuevodia.com/noticias/seguridad"

while True:
    logging.info("    ********** STARTING SCAN **********")
    
    logging.info("    Getting current articles")
    # Get the current articles in endi.com 
    # under the Seguridad category
    articles = current_artcls(news_url)
    
    logging.info("    Iterating over current articles")
    logging.info('\n')
    # Iterate over current articles
    for article in articles:
        # Re-establish database connection
        db.reconnect()
        # Create communication cursor object
        cursor = db.cursor(buffered=True)

        # Get article hash
        art_hash = get_hash(article=article)
        # Fetch stored articles hashes
        cursor.execute(querys.FETCH_HASHES)
        # Select rows where article hash exists
        cursor.execute(querys.CHECK_HASH, [art_hash])
        # Count number of rows hash appears
        check = cursor.rowcount

        # Get article data and store to database only if
        # article hash do not exists; check variable must
        # be 0
        if check == 0:
            logging.info("    + + + New article found!")
            # Create data dictionary with extracted article initial
            # data and hash 
            # URL, Headline, Author, and Hash 
            query_dict = artcl_data(article=article)
            # Update data dictionary to store content data
            # Subheadline, Datetime, and Content
            query_dict.update(artcl_content(article_data=query_dict))
            
            # Insert article data into database table Articles
            logging.info("    Writing article data in database")
            cursor.execute(querys.INSERT_ARTICLE, query_dict)
            # Commit the insert
            db.commit()

            # Get ID of inserted article
            art_id = cursor.lastrowid

            # Create list with article detected location 
            locs_found = detect_location(article_data=query_dict)
            # Create list with detected locations validated
            loc_validated = validate_location(location=locs_found)
            
            # Insert into ArticleLocationRelationship only if
            # valudad location contains values 
            if loc_validated:
                logging.info("    Location validated")
                # Iterate over validated locations
                for loc in loc_validated:
                    # Get the location id
                    loc_id = get_location_id(validated_location=loc)
                    
                    logging.info("    Writing in bridge table")
                    # Insert ArticleID and LocationID into ArticlesLocationRelation
                    query_dict = {"articleid": art_id, "locationid": loc_id}
                    cursor.execute(querys.INSERT_ARTICLE_LOCATION, query_dict)
                    db.commit()

                    logging.info("    Updating location relevance score")
                    # Calculate relevance score for the given location
                    sc = score(location_id=loc_id)
                    # Update the location relevance score
                    query_dict = {"locationid":loc_id , "score": sc}
                    cursor.execute(querys.UPDATE_RELEVACE_SCORE, query_dict)
                    db.commit()
            logging.info("    Done with article")
            logging.info('\n')
        else:
            logging.info("    Article exists in database")
            logging.info('\n')
        cursor.close()
        db.close()
    logging.info("    ********** ENDING SCAN **********")
    logging.info("    ********** Waiting 30 mins for next scan at: [%s] **********", 
                 datetime.now() + timedelta(minutes=30))
    time.sleep(1800)
