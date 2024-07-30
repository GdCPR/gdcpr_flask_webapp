import spacy
from unidecode import unidecode
from database_manager.database_connector import dbconnection as db

# Load the model
npl= spacy.load("es_core_news_sm")

def detect_location(article_data: dict) -> list:
    """
    Detect location from article headline, subheadline, and content.
    """    

    # Get article content
    body_text = unidecode(article_data["content"])
    headline_sub_text = unidecode(article_data["subheadline"])
    headline_text = unidecode(article_data["headline"])

    # Analyze article content
    body_doc = npl(body_text)
    headline_doc = npl(headline_text)
    headline_sub_doc = npl(headline_sub_text)

    # Store the pueblos found from the article content
    loc_found_body = [ent.text.lower().replace(" ", "_")
                                 for ent in body_doc.ents if ent.label_== "LOC"]

    loc_found_headline_sub = [ent.text.lower().replace(" ", "_")
                                         for ent in headline_sub_doc.ents if ent.label_== "LOC"]

    loc_found_headline = [ent.text.lower().replace(" ", "_")
                                     for ent in headline_doc.ents if ent.label_== "LOC"]
    
    loc_found = list(set(loc_found_body + loc_found_headline_sub + loc_found_headline))

    return loc_found

def validate_location(location: list) -> set:
    """
    """
    # Create database cursor object
    db.reconnect()
    cursor = db.cursor()

    # Retrieve locations from database
    query = """SELECT NormalizedName FROM Location"""
    cursor.execute(query)

    # Fetch all rows
    locs_fetch = cursor.fetchall()

    # Create a list from row Name fields
    locs_official = [row[0] for row in locs_fetch] # type: ignore

    locs_validated = set(location) & set(locs_official)

    return locs_validated

def get_location_id(validated_location: str) -> int: # type: ignore
    """
    """
    # Create database cursor object
    db.reconnect()
    cursor = db.cursor()

   # Retrieve locations from database
    query = """SELECT * FROM Location"""
    cursor.execute(query)

    # Fetch all rows
    locs_fetch = cursor.fetchall()
    
    # Retrieve location id from database
    for row in locs_fetch:
        if validated_location == row[2]:
                return row[0]
