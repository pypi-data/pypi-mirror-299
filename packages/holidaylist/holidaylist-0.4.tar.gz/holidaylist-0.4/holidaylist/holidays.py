import requests

def get_holidays(api_key, params):
    holidays_url = "https://back.holidaylist.io/api/v1/holidays/"
    
    # Ensure the API key is included in the parameters
    params['key'] = api_key
    
    response = requests.get(holidays_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch holidays. Status code: {response.status_code}"}
