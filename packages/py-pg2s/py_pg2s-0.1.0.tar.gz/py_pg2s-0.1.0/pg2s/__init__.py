import os
import gensim.downloader as api
from sentence_transformers import SentenceTransformer
import spacy
from spacy.cli import download

try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("Model en_core_web_sm not found. Downloading...")
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
    
wv = api.load('word2vec-google-news-300')  
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')