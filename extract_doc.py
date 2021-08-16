# scrap cse document
# summarize docs
import requests
import os
import pdftotext

def dl_doc_from_url(url, filename):
    r = requests.get(url, allow_redirects=True)

    with open(filename, 'wb') as f:
        f.write(r.content)

def mk_dir(new_dir):
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

def handle_logic(dataDict = {
    "url": None,
    "path": None
}):
    dl_doc_from_url(dataDict.get("url"), dataDict.get("path"))

    extract_from_file(dataDict.get("path"))

def extract_from_file(path: str):
    # If it's password-protected
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # How many pages?
    print(len(pdf))

    # Iterate over all the pages
    for page in pdf:
        print(page)

    # Read some individual pages
    print(pdf[0])
    print(pdf[1])

    # Read all the text into one string
    print("\n\n".join(pdf))

handle_logic({"url": "https://webfiles.thecse.com/Peak_Fintech_Continues_Expansion_of_Business_Hub_with_Addition_of_Two_New_Banks_and_New_Office_in_Guangzhou.pdf?dcWC2NW_GzmSFbHOadxyHNESnqSpHkza", "path": "PKK_Peak_Fintech_Continues_Expansion_of_Business_Hub_with_Addition_of_Two_New_Banks_and_New_Office_in_Guangzhou.pdf?dcWC2NW_GzmSFbHOadxyHNESnqSpHkza.pdf"})
