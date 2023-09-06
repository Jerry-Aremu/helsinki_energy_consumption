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
    property_list = requests.get(api_url)
    if property_list.status_code !=200:
        print(f"request error:{property_list.status_code}")
    else:
        property_list_data = property_list.text
        property_list_df = pd.read_json(property_list_data)
        return property_list_df 
    
    
    
# get hourly, daily or monthly data depending on set constraints 

def get_request_as_df(
    period =None,
    record=None,
    search_string=None,
    reporting_group=None,
    start_time=None,
    end_time=None,
    Normalization=False,
    version=None
):
    
    """
       this function returns energy consumption data based on the constraints that are set the list 
       of valid constraints are as shown below:
       Period: hourly, daily or monthly 
       Record: LocationName, PropertyCode, PurposeOfUse, BuildingCode  
       ReportingGroup: Electricity, Heat, Water, DistrictCooling
       StartingTime: example <2019-01-01>
       EndTime: example <2091-01.01>
       Version: V1.0   
    """
    
# get a dictionary of all possible arguement
    all_args = locals()

    # reset the dictionary depending on whether the "Heat" is selected as reporting group or not
    set_args = {k: v for k,v in all_args.items() if v is not None}
    if set_args['Normalization'] == False:
        del set_args['Normalization']
        

        #get a list of values set from the "set_args" dictionary
        set_arg_list = list(set_args.values())

        if 'PropertyCode' in list(set_args.values()):
            # construct the url for API access based on the selected contsraints
            url = 'https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/{}/ListByProperty?Record={}&SearchString={}&ReportingGroup={}&StartTime={}&EndTime={}'
            period_, record_, search_string_, reporting_group_, start_time_, end_time_= set_arg_list[0],set_arg_list[1],set_arg_list[2],set_arg_list[3],set_arg_list[4], set_arg_list[5]
            access_link1 = url.format(period_, record_, search_string_, reporting_group_, start_time_, end_time_)
            response1 = requests.get(access_link1)
            data1 = response1.text
            data_df1 = pd.read_json(data1)
            return data_df1
        else:
            # construct the url for API access based on the selected contsraints
            record_variant = set_arg_list[1].replace(" ","%20")
            url = 'https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/{}/ListByProperty?Record={}&SearchString={}&ReportingGroup={}&StartTime={}&EndTime={}'
            period_2, record_2, search_string_2, reporting_group_2, start_time_2, end_time_2 = set_arg_list[0], record_variant, set_arg_list[2], set_arg_list[3], set_arg_list[4], set_arg_list[5]
            access_link2 = url.format(period_2, record_2, search_string_2, reporting_group_2, start_time_2, end_time_2)
            response2 = requests.get(access_link2)
            data2 = response2.text
            data_df2 = pd.read_json(data2)
            return data_df2    
        
    
    else:
        set_arg_list = list(set_args.values())

         

        if 'PropertyCode' in list(set_args.values()):
            # construct the url for API access based on the selected contsraints
            url = 'https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/{}/ListByProperty?Record={}&SearchString={}&ReportingGroup={}&StartTime={}&EndTime={}&Normalization={}'
            period_, record_, search_string_, reporting_group_, start_time_, end_time_, normalization_ = set_args_list[0],set_args_list[1],set_args_list[2],set_args_list[3],set_args_list[4], set_args_list[5],set_args_list[6]
        
            access_link1 = url.format(period_, record_, search_string_, reporting_group_, start_time_, end_time_, normalization_)
            response1 = requests.get(access_link1)
            data1 = response1.text
            data_df1 = pd.read_json(data1)
            return data_df1
        else:
            # construct the url for API access based on the selected contsraints
            record_variant = set_arg_list[1].replace(" ","%20")
            url = 'https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/{}/ListByProperty?Record={}&SearchString={}&ReportingGroup={}&StartTime={}&EndTime={}'
            period_2, record_2, search_string_2, reporting_group_2, start_time_2, end_time_2 = set_arg_list[0], record_variant, set_arg_list[2], set_arg_list[3], set_arg_list[4], set_arg_list[5]
            access_link2 = url.format(period_2, record_2, search_string_2, reporting_group_2, start_time_2, end_time_2)
            response2 = requests.get(access_link2)
            data2 = response2.text
            data_df2 = pd.read_json(data2)
            return data_df2
            

            
def get_daily_energy_for_a_specified_year(start_date, end_date):
    
    df1 = pd.read_json('data.json')

    # list of location names with space replacement
    location_names = [location.replace(" ", "%20") for location in df1['locationName']]

    # List to store URLs with valid JSON data
    valid_urls = []

    # Fetching data for each location
    for location in location_names:
    
        url = f"https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/Daily/ListByProperty?Record=LocationName&SearchString={location}&ReportingGroup=Electricity&StartTime={start_date}&EndTime={end_date}"
        response = requests.get(url)
        data = response.json()
        if 'errorCode' not in data or data['errorCode'] != 'MissingSettingsException':
            valid_urls.append(url)

        
    # Creating a folder to store the JSON files
    folder_name = "energy_data"
    os.makedirs(folder_name, exist_ok=True)
    
    # Save data from each valid URL as a separate JSON file in the folder
    for index, url in enumerate(valid_urls):
        response = requests.get(url)
        data = response.json()
        filename = f"data_{index}.json"
        file_path = os.path.join(folder_name, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)
    print(f"Data saved for URL: {url} (filename: {filename})")

    print("Data saved successfully.")
    
    # Read the JSON file into a pandas DataFrame
    df = pd.read_json('merged_data.json')
    print(f"the shape of the dataframe is: {df.shape}")
    return df.head()  
    


