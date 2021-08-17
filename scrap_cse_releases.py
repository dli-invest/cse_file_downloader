import pandas as pd
import time
import os
import requests
import json
from cad_tickers.exchanges.cse import get_recent_docs_from_url
from extract_doc import dl_doc_from_url, mk_dir
from io import BytesIO

def fig_to_buffer(fig):
  """ returns a matplotlib figure as a buffer
  """
  buf = BytesIO()
  fig.savefig(buf, format='png')
  buf.seek(0)
  imgdata = buf.read()
  return imgdata

def make_discord_request(content, filename, file):
    url = os.getenv("DISCORD_WEBHOOK")
    if url == None:
        print('DISCORD_WEBHOOK Missing')
        pass
    data = {}
    data["content"] = content
    resp = requests.post(
        url, data=json.dumps(data),  headers={"Content-Type": "application/json"}
    )

    # print(resp)
    # print(resp.content)
    files = {'file': (filename, file, 'application/pdf')}
    resp = requests.post(
        url, files=files
    )
    print(resp)
    print(resp.content)

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
            # wrap in todo
            stock_doc_dir = f"docs/{stockName}"
            mk_dir(stock_doc_dir)
            stock_doc_file_path = docUrl.split("/")[-1]
            pdf_file_name = f"{stock_doc_dir}/{stock_doc_file_path}.pdf"
            file_contents = dl_doc_from_url(docUrl, pdf_file_name)
            make_discord_request(f"*{stockName}*: \n {docUrl}", pdf_file_name, file_contents)
            time.sleep(2)
            exit(1)
        else:
            pass

df = df.sort_values(by=['stock'])
df.to_csv(csv_file, index=False)