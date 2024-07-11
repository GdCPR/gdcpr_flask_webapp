def print_dict(d):
    """Print dictionary in a more readable format."""
    # From: https://www.geeksforgeeks.org/python-pretty-print-a-dictionary-with-dictionary-value/
    #take empty string
    pretty_dict = ''  
        
    #get items for dict
    for k, v in d.items():
        pretty_dict += f'{k}: \n'
        for value in v:
            pretty_dict += f'    {value}: {v[value]}\n'
    #return result
    return pretty_dict