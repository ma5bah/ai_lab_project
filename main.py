from PyPDF2 import PdfReader
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
# disable cors
# CORS(app)
CORS(app, resources={r"/upload": {"origins": "http://localhost:8000"}})


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()


def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


class PDFWrapper:
    def __init__(self, pdf_name):
        self.name = pdf_name
        self.text = ""

    def read(self):
        reader = PdfReader(self.name)
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            self.text = self.text + "\n" + text
        return self.text


def check_plagiarism(first_pdf, second_pdf):
    first = PDFWrapper(first_pdf)
    second = PDFWrapper(second_pdf)
    vectors = vectorize([first.read(), second.read()])
    sim_score = similarity(vectors[0], vectors[1])[0][1]
    return sim_score


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return "Missing PDF files", 400

    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']

    return "Plagiarism score: " + str(check_plagiarism(pdf1, pdf2) * 100)


if __name__ == '__main__':
    app.run(debug=True)

# print(check_plagiarism("1706.03762.pdf", "1706.03762.pdf"))
