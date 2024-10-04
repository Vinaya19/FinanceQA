import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from text_extraction import get_text

def remove_special_characters(text):
    # removing characters except alphabets, numbers and spaces
    text_without_special_characters = re.sub(r'[^a-zA-Z0-9\s]','', text)
    return text_without_special_characters

def convert_text_to_lowercase(text):
    # converting all text to lowercase
    return text.lower()

def tokenise_text(text):
    # converting text to tokens using nltk library
    tokenised_text = word_tokenize(text)
    return tokenised_text

def remove_stopwords(tokenised_text):
    stopwords_list = set(stopwords.words('english'))

    # tokens of the text without stopwords
    filtered_tokenised_text = []

    for token in tokenised_text:
        if token not in stopwords_list:
           filtered_tokenised_text.append(token)
    return filtered_tokenised_text
           
def lemmatize_tokenised_text(tokenised_text):
    lemmatized_tokens_list = []
    filtered_text = ''

    # reducing words into their lemma form
    lemmatizer = WordNetLemmatizer()

    for token in tokenised_text:
        lemmatized_tokens_list.append(lemmatizer.lemmatize(token))
    return lemmatized_tokens_list

def preprocessing_inputText(text):
    # Step - 1: removing special characters from text
    cleaned_text = remove_special_characters(text)

    # Step - 2: Converting text into a list of tokens
    tokenised_text = tokenise_text(convert_text_to_lowercase(cleaned_text))

    # Step - 3: Removing stopwords from tokens
    filtered_tokenised_text = remove_stopwords(tokenised_text)

    # Step - 4: Performing Lemmatization on pre-processed text
    lemmatized_tokenised_text = lemmatize_tokenised_text(filtered_tokenised_text)

    # final preprocessed text
    preprocessed_text = ' '.join(lemmatized_tokenised_text)
    return preprocessed_text


if __name__=='__main__':
    '''input_text = "##The quick brown foxes are jumping over the lazy dogs???!!!"
    pre_processed_text = remove_special_characters(input_text)
    print("Text after removing special characters ", pre_processed_text)

    tokenised_text = tokenise_text(convert_text_to_lowercase(pre_processed_text))
    print("Tokens list of the input text ", tokenised_text)

    filtered_tokenised_text = remove_stopwords(tokenised_text)
    print("Tokens list of the input text after removing stopwords ", filtered_tokenised_text)

    lemmatized_tokenised_text = lemmatize_tokenised_text(filtered_tokenised_text)
    print("Tokens of text in their root form ",lemmatized_tokenised_text)'''

    preprocessed_text = preprocessing_inputText(get_text("./2023_Annual_Report.pdf"))
