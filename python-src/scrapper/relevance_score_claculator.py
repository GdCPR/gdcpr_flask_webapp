from database_manager.database_connector import dbconnection as db
from database_manager import querys

def calculate_score(location_id: int):
    """
    """
    # SELECT COUNT(*) FROM table_name WHERE condition
    # get location id
    # count of location id found in articles
    # count total articles
    # divide location found and total articles
    db.reconnect()
    cursor = db.cursor(buffered=True)
    
    # Create dict to send to query
    data = {"locationid": location_id}
    
    # Execute qury to count
    cursor.execute(querys.COUNT, data) # type: ignore

    # Fetch result and extract the value from returned tuple
    loc_count = int(cursor.fetchone()[0]) # type: ignore

    # Fetch last row with max id from Articles table, extract ID
    cursor.execute(querys.ARTICLE_MAXID)
    arts_count = int(cursor.fetchone()[0]) # type: ignore

    score = loc_count/arts_count
    
    return score