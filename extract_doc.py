# scrap cse document
# summarize docs
import requests
import os
import pdftotext

def dl_doc_from_url(url, filename):
    r = requests.get(url, allow_redirects=True)

    with open(filename, 'wb') as f:
        f.write(r.content)
    
    return r.content


def post_image_to_discord(url: str, file: str, filename: str = 'file'):
  url = url
  result = requests.post(
      url, files={filename: file}
  )

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Image Delivered {}.".format(result.status_code))

def mk_dir(new_dir):
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

def handle_logic(dataDict = {
    "url": None,
    "path": None
}):
    dl_doc_from_url(dataDict.get("url"), dataDict.get("path"))

    pdf_text = extract_from_file(dataDict.get("path"))

    parts = dataDict.get("path").split(".")
    txt_path = "".join(parts[:-1] + [".txt"])
    # save file as text
    with open(txt_path, "w") as f:
        f.write(pdf_text)

def extract_from_file(path: str):
    # If it's password-protected
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Iterate over all the pages
    for page in pdf:
        print(page)

    # Read all the text into one string
    pdf_pages = "\n\n".join(pdf)
    return pdf_pages

handle_logic({"url": "https://webfiles.thecse.com/Peak_Fintech_Continues_Expansion_of_Business_Hub_with_Addition_of_Two_New_Banks_and_New_Office_in_Guangzhou.pdf?dcWC2NW_GzmSFbHOadxyHNESnqSpHkza", "path": "docs/PKK_Peak_Fintech_Continues_Expansion_of_Business_Hub_with_Addition_of_Two_New_Banks_and_New_Office_in_Guangzhou.pdf?dcWC2NW_GzmSFbHOadxyHNESnqSpHkza.pdf"})
