import pandas as pd
import time
import os
import requests
import json
from cad_tickers.exchanges.cse import get_recent_docs_from_url

def make_discord_request(content):
    url = os.getenv("DISCORD_WEBHOOK")
    if url == None:
        print('DISCORD_WEBHOOK Missing')
        pass
    data = {}
    data["content"] = content
    result = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    print(result)

# list of stocks with urls to cse listing page
stockUrls = [
{
    "stock": "PKK",
    "url": "https://www.thecse.com/en/listings/technology/peak-fintech-group-inc"
},
{
    "stock": "IDK",
    "url": "https://www.thecse.com/en/listings/diversified-industries/threed-capital-inc"
},
{
    "stock": "ACDC",
    "url": "https://www.thecse.com/en/listings/technology/extreme-vehicle-battery-technologies-corp"
},
{
    "stock": "VPH",
    "url": "https://www.thecse.com/en/listings/life-sciences/valeo-pharma-inc"
},
{
    "stock": "VST",
    "url": "https://www.thecse.com/en/listings/technology/victory-square-technologies-inc"
},
{
    "stock": "ACT",
    "url": "https://thecse.com/en/listings/technology/aduro-clean-technologies-inc"
}
]

csv_file = "docs.csv"
if os.path.isfile(csv_file):
    # read from csv
    df = pd.read_csv(csv_file)
else:
    # make new df
    df = pd.DataFrame(columns=["stock", "url", "docUrl"])

# read data from csv 
for stock in stockUrls:
    stockName = stock.get("stock")
    stockUrl = stock.get("url")

    urls = get_recent_docs_from_url(stockUrl)
    
    for docUrl in urls:
        # skip malformed relative urls
        if docUrl[0] == '/':
            continue
        # add each element to list
        exists = docUrl in df["docUrl"].tolist()
        if exists == False:
            print(f"Adding {stockName}: {docUrl}")
            df.loc[len(df)] = [stockName, stockUrl, docUrl]
            make_discord_request(f"*{stockName}*: \n {docUrl}")
            time.sleep(2)
        else:
            print(f"Not adding url")
df = df.sort_values(by=['stock'])
df.to_csv(csv_file, index=False)