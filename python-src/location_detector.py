import spacy
import pandas as pd
from unidecode import unidecode

# Load the model
npl= spacy.load("es_core_news_sm")

# Store html tables
# df_wiki= pd.read_html("https://en.wikipedia.org/wiki/Pueblos_in_Puerto_Rico#List_of_Pueblos")
municipalities_df = pd.read_csv("resources/puerto_rico_municipalities.txt",
                                sep= " ",
                                header= None,
                                names= ["municipality"])

# Filter for the first table and unique values from the Pueblos Column
municipalities_list= [unidecode(municipality) for municipality in municipalities_df["municipality"].values]

def detect_location(article_data: dict) -> dict:
    """
    """
    # Get article content
    body_text= unidecode(article_data["content"])
    headline_sub_text= unidecode(article_data["headline_sub"])
    headline_text= unidecode(article_data["headline"])

    # Analyze article content
    body_doc= npl(body_text)
    headline_doc= npl(headline_text)
    headline_sub_doc= npl(headline_sub_text)

    # Store the pueblos found from the article content
    municipalities_found_body= [ent.text.lower().replace(" ", "_") for ent in body_doc.ents if ent.label_== "LOC"]
    municipalities_found_headline_sub= [ent.text.lower().replace(" ", "_") for ent in headline_sub_doc.ents if ent.label_== "LOC"]
    municipalities_found_headline= [ent.text.lower().replace(" ", "_") for ent in headline_doc.ents if ent.label_== "LOC"]

    municipalities_validated= (set(municipalities_found_headline) & set(municipalities_list)) or (set(municipalities_found_body) & set(municipalities_list)) or (set(municipalities_found_headline_sub) & set(municipalities_list))
    return {"municipality": list(municipalities_validated)}