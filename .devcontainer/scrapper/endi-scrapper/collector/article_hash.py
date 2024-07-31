import hashlib
from bs4 import element

def get_hash(article: element.Tag) -> str:
    """
    Maps article tag objecto to fixed-size value

    
    """
    # Create a hash object
    hash_object = hashlib.sha256(article.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()

    return hex_digest