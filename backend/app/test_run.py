import requests

def test_get_all_cards():
    url = "http://172.17.0.4:5000/cards/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Test Passed: Successfully fetched all cards")
            print("Response:", response.json())
        else:
            print("Test Failed: Unable to fetch all cards")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Test Failed: Exception occurred")
        print("Exception:", str(e))

if __name__ == "__main__":
    test_get_all_cards()
