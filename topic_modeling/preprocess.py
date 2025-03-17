import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
# nltk.download('punkt')

nltk.data.path.append('/Users/shrabanighosh/nltk_data')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('wordnet')
# nltk.download('stopwords')



def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    return text.strip()

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return " ".join([word for word in text.split() if word not in stop_words])

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    return " ".join([lemmatizer.lemmatize(word) for word in words])

def stemming_text(text):
    stemmer = PorterStemmer()
    # text = "assessing restoring reproducibility jupyter notebook"
    tokens = word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in tokens]
    print(" ".join(stemmed_words)) 

# def preprocess_title(title):
#     title = clean_text(title)
#     title = remove_stopwords(title)
#     title = lemmatize_text(title)
#     # title = remove_custom_stopwords(title)
#     # title = filter_titles(title)
#     return title

def preprocess(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Remove punctuation and numbers
    words = word_tokenize(text)  # Tokenize
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]  # Apply stemming
    return ' '.join(words)

def title_preprocess(filename):
    # filename = 'dblp_dm_filtered_2000_2025.csv'

    df = pd.read_csv(filename)
    print(df.shape)
    # df = df[df['booktitle'] == 'ICSE']
    # print(df)
    yearrange = list(range(2012, 2026, 1)) #[2000 to 2025]
    df = df[df['year'].isin(yearrange)]
    data = df['year'].value_counts().reset_index()
    print(data)
    df['preprocessed_title'] = df['title'].fillna('').apply(preprocess)
    df = df[['authors_name', 'title','preprocessed_title' ,'pages', 'year',
           'data', 'key', 'ee', 'url', 'booktitle', 'crossref'
           ]]
    # df.to_csv('dblp_dm_filtered_2012_2025.csv')
    return df
# titles = df.title.tolist()
# preprocessed_titles = [preprocess_title(title) for title in titles]
# print(preprocessed_titles)
# print(df.shape)