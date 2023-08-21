import requests
from flask import Flask
import re
import json
from flask_cors import CORS


app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://example.com"])

def parse_text_to_dict(text):
    records = []
    current_record = {}
    
    for line in text.strip().split('\n'):
        if line.startswith('found='):
            continue
        
        match = re.match(r'records\[(\d+)\]\.(.+)', line)
        if match:
            index, field = match.groups()
            index = int(index)
            if index >= len(records):
                records.append(current_record)
                current_record = {}
            
            value = line.split('=', 1)[-1]
            value = value.replace('\r', '') 
            
            key = re.sub(r'\[.*\]|=.*', '=', field)
            
            current_record[key] = value
    
    if current_record:
        records.append(current_record)
    
    return {'found': len(records), 'records': records}


def convert_to_json(data):
    return json.dumps(data, indent=4)

@app.route('/')
def hello():
    return "Application intelbras API - ON"

@app.route('/get_users/<device_ip>/<device_port>/<username>/<password>')
def get_all_users(device_ip, device_port, username, password):
    url = "http://{}:{}/cgi-bin/recordFinder.cgi?action=doSeekFind&name=AccessControlCard&count=4300".format(
        str(device_ip),
        str(device_port)
    )
    digest_auth = requests.auth.HTTPDigestAuth(username, password)
    response = requests.get(url, auth=digest_auth, timeout=20, verify=False)
    
    if response.status_code == 200:
        parsed_data = parse_text_to_dict(response.text)
        json_data = convert_to_json(parsed_data)
        return json_data
    else:
        return "Failed to fetch software version."

@app.route('/remove_user/<device_ip>/<device_port>/<username>/<password>/<userid>')
def remove_user_users(device_ip, device_port, username, password, userid):
    url = "http://{}:{}/cgi-bin/AccessUser.cgi?action=removeMulti&UserIDList[0]={}".format(
        str(device_ip),
        str(device_port),
        str(userid)
    )
    digest_auth = requests.auth.HTTPDigestAuth(username, password)
    response = requests.get(url, auth=digest_auth, timeout=20, verify=False)
    
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to fetch software version."

@app.route('/get_software_version/<device_ip>/<device_port>/<username>/<password>')
def get_software_version(device_ip, device_port, username, password):
    url = "http://{}:{}/cgi-bin/magicBox.cgi?action=getSoftwareVersion".format(
        str(device_ip),
        str(device_port)
    )
    digest_auth = requests.auth.HTTPDigestAuth(username, password)
    response = requests.get(url, auth=digest_auth, timeout=20, verify=False)
    
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to fetch software version."

@app.route('/get_temparature/<device_ip>/<device_port>/<username>/<password>')
def get_temperature(device_ip, device_port, username, password):
    url = "http://{}:{}/cgi-bin/configManager.cgi?action=getConfig&name=MeasureTemperature".format(
        str(device_ip),
        str(device_port)
    )
    digest_auth = requests.auth.HTTPDigestAuth(username, password)
    response = requests.get(url, auth=digest_auth, timeout=20, verify=False)
    
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to fetch software version."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
