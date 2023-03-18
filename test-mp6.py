import requests
import json

url = 'https://u46j45y1h6.execute-api.us-east-1.amazonaws.com/prod/'

payload = {
			"submitterEmail": "", # <insert your coursera account email>,
			"secret": "", # <insert your secret token from coursera>,
			"dbApi": "" # insert your API Gateway Post method invoke URL
		}
print(json.dumps(payload))
r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)
