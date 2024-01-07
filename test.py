import docx

doc = docx.Document("test_doc_2.docx")
for paragraph in doc.paragraphs:
    print(paragraph.text)