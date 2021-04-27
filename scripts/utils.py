import json 

def read_json(input_path: str) -> dict: 
    """
    Reads a json file
    
    Arguments:
    ----------
        input_path: path to json file
    
    Returns
    -------
        dict
    """
    
    with open(input_path, 'r') as jfile:
        jdict = json.load(jfile)
    
    return jdict

def write_json(jdict: dict, output_path: str ) -> None:
    """
    Writes a dictionary to a json file. 
    
    Arguments:
    ----------
        jdict: dictionary
        output_path: path to write json file
    
    Returns
    -------
        None
    """
    with open(output_path, 'w') as jfile: 
        json.dump(jdict, jfile)
        
def read_file(input_path: str) -> list: 
    """
    Reads a txt file.
    
    Arguments:
    ---------
        input_path: path to txt file
    
    Returns
    -------
        list
    """
    with open(input_path, 'r') as file: 
        text_list = file.readlines()
        text_list = [line.replace('\n', '') for line in text_list]
    return text_list