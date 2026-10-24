import requests
def check_internet_connection():
    try:
        response=requests.get("https://www.google.com",timeout=3)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False