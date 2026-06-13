import re
import pandas as pd

def clean_description(text):
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([^a-zA-Z\s])', r' \1 ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    text = text.lower()
    return " ".join(text.split())

def normalize_genres(genres, n=4):
    if not isinstance(genres, list):
        return ''
    return ' '.join(
        g.lower().replace(' ', '') for g in genres[:n]
    )
def normalize_author(author):
    if not isinstance(author, str):
        return ''
    return author.lower().replace(' ', '')
def normalize_pages(pages):
    if pd.isna(pages):
        return ''
    
    if pages < 200:
        return 'shortbook'
    elif pages < 500:
        return 'mediumbook'
    else:
        return 'longbook'

def normalize_year(year):
    if pd.isna(year):
        return ''

    if year < 1950:
        return 'classicera'
    elif year < 2000:
        return 'modernera'
    else:
        return 'contemporaryera'

STOPWORDS = {
    "the", "of", "and", "to", "in", "a", "an", "for", "on", "with", "book"
}
def has_token_overlap(a, b, min_common=2):
    tokens_a = {t for t in a.lower().split() if t not in STOPWORDS and not t.isdigit()}
    tokens_b = {t for t in b.lower().split() if t not in STOPWORDS and not t.isdigit()}
    return len(tokens_a & tokens_b) >= min_common