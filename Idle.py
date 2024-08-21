import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary to store User IDs and Names
user_library = {
    "ZDyUl2g7_AIm-bjf": "Angelie Buen",
    "Yqc_g7x-2IwCx0-K": "Bryce Gabehart",
    "ZZSJ2FIXzgIJctGV": "Courtney Lynn Beldon",
    "Zb-NdarzmaWe75RM": "Dominic Leyva",
    "YsQPMZXzuGmI-uHT": "Jayson Pare",
    "ZcPf3Vr-F9ocLYB6": "Jeanelle Villaluna",
    "ZpY0hsJPit9MkRlN": "Jherard Marc Catolos",
    "Yz9AknuUVgvWQ9Kz": "Jhovenell Manait",
    "Y4qSP3W3AGI0jUlS": "Jimm Claude Tapawan",
    "ZPo6AWMsaLZEU7CL": "John Carlos Diaz",
    "ZPXZJSdnk9_Kn21w": "Joseph Ryan Cruz",
    "ZYIM1urVPZ6vBAuS": "Karlo Miguel Teves",
    "ZhJ96___-o5bMp1f": "Kethlyn Joy Dennis",
    "Zazsh20hXrKx2YEc": "Larry Ivan Young",
    "ZT4_AOBtQ9g8EXp9": "Marc Philip Turtal",
    "ZpTHtszmot7cEyrk": "Michael Angelo Vasquez",
    "Y2F9mvlX43mROHoW": "Michael Ian Alvarez",
    "ZOkR_PTJgd_jRPu8": "Miguel Angelo Villanueva",
    "Zk5Jov3wNgGEeqQ0": "Monica Louise Lavilla",
    "ZiUFxDGD37RlR-V6": "Nicolas Eduardo Huet",
    "ZLSagPW8cdXBsAJ_": "Rafael Luigi Cartera",
    "Y7mo46IRYy0qKlRk": "Randy Luyao",
    "ZSmecIHYzmIO8oWX": "Rensy Lomboy",
    "ZVHtAmlKFQkZYUzq": "Riz Mark Corpuz",
    "ZKLUblcCTyfcyHXx": "Robert John Comanda",
    "ZZLGyyVaPj-rDRKZ": "Sherm Rei Cervantes",
    "ZrBkYjnNHM-Sza92": "Szer Dave Victorino",
    "ZJTj9ZbpqIy5TfaE": "Thony Danille Labrador",
    "Zhu5WrVwfv_OVqSV": "Victoria Grace Gonzaga"
}

def login():
    url = "https://api2.timedoctor.com/api/1.0/login"
    body = json.dumps({
        "email": "bryce.gabehart@myamazonguy.com",
        "password": "Gabehart01!",
        "permissions": "write"
    })
    headers = {
        "Content-Type": "application/json"
    }
    resp = requests.post(url=url, data=body, headers=headers)
    resp_json = resp.json()
    return resp_json['data']['token']

def fetch_user_weekly_idle_percentage(user_id, start_date, end_date):
    token = login()  # Fetch the token using the login function
    idle_url = f"https://api2.timedoctor.com/api/1.0/stats/summary-ratio?company=YFpYQwOkUAAEWZlH&user={user_id}&from={start_date}&to={end_date}&token={token}"
    
    headers = {
        'accept': 'application/json'
    }
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            response = requests.get(idle_url, headers=headers)
            
            if response.status_code == 200:
                idle_json_response = response.json()
                if (idle_json_response and 'data' in idle_json_response 
                        and 'users' in idle_json_response['data'] 
                        and len(idle_json_response['data']['users']) > 0):
                    idle_data = idle_json_response['data']['users'][0]
                    idle_percentage = round(idle_data.get('idleMinsRatio', 0) * 100, 2)
                    return f"User {user_library.get(user_id, 'Unknown User')}'s Idle Percentage: {idle_percentage}%"
            else:
                return f'Error fetching idle percentage: {response.text}'
        except Exception as error:
            return f'Error while making API call: {error}'
        
        attempts += 1

    return f"User {user_library.get(user_id, 'Unknown User')}'s Idle Percentage: 0%"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_idle_percentage', methods=['POST'])
def fetch_idle_percentage():
    user_name = request.form['user_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Reverse lookup: Find the user ID based on the name
    user_id = next((uid for uid, name in user_library.items() if name.lower() == user_name.lower()), None)

    if user_id:
        result = fetch_user_weekly_idle_percentage(user_id, start_date, end_date)
    else:
        result = "User name not found in the library."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
