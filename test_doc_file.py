# pip install docx
from docx import Document
from extract_doc import dl_pdf_doc_from_url

file_path = "/workspaces/cse_file_downloader/docs/ACT/test.docx"
doc_content = dl_pdf_doc_from_url("https://webfiles.thecse.com/ACT-_SSN_Virtual_Event_Final.docx?YcYs3CxdF2jpqqLUCSAX9aVNx5T_Envg", file_path)


with open(file_path, "rb") as doc_file:
    document = Document(doc_file)

print(document)
docu=""
for para in document.paragraphs:
    docu += para.text
#to see the output call docu
print(docu)