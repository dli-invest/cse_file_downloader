import pandas as pd
import time
import os
from cad_tickers.exchanges.cse import get_recent_docs_from_url
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
        else:
            print(f"Not adding url")
    time.sleep(1)

df.to_csv(csv_file, index=False)