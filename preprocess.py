import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Extract text from PDF
def get_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        read_file = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in read_file.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    pdf_path = "/Users/vinayabomnale/Desktop/Code/nlp_project/2023_Annual_Report.pdf"
    raw_text = get_text(pdf_path)
    print(raw_text)