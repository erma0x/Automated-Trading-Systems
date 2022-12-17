import requests
import json

Set the API endpoint
endpoint = "https://api.binance.com/api/v3/orderbook/ticker"

Set the parameters for the request
params = {
"symbol": "BTCUSDT"
}

Make the request to the API
response = requests.get(endpoint, params=params)

Convert the response to a JSON object
data = response.json()

Print the response data
print(json.dumps(data, indent=4))

Open a file for writing the orderbook data
with open("orderbook_data.json", "w") as f:
# Write the data to the file in JSON format
json.dump(data, f)

print("Orderbook data saved to file.")
