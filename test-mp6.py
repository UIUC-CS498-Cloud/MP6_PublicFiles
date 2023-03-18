import requests
import json

url = 'https://u46j45y1h6.execute-api.us-east-1.amazonaws.com/prod/'

payload = {
			"submitterEmail": "", # <insert your coursera account email>,
			"secret": "", # <insert your secret token from coursera>,
			# "partId" : "G6U3L"
			"dbApi": "https://sfb734j9r7.execute-api.us-east-1.amazonaws.com/test/mp11"
		}
print(json.dumps(payload))
r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)
