import requests
import warnings
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as datetime


# function for fetching the total list of properties 
def total_list_of_properties(api_url):
    
    """ 
    this function gets the total list of Helsinki utility and service properties
    Example: 1000 Hakaniemen kauppahalli, 1001 Hietalahden kauppahalli e.t.c  
        
    """ 
    property_list = requests.get(property_list_url)
    if property_list.status_code !=200:
        print(f"request error:{property_list.status_code}")
    else:
        property_list_data = property_list.text
        property_list_df = pd.read_json(property_list_data)
        return property_list_df      
