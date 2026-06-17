import pandas as pd

from scripts.scoring import weighted_rating
from scripts.utils.text_utils import (
    clean_description,
    normalize_author,
    normalize_genres,
    normalize_pages
)

def prepare_books_dataset():
    books = pd.read_json('dataset.json')

    books_wo_duplicates = books.sort_values(by='num_ratings', ascending=False).drop_duplicates(subset=['title', 'author'], keep='first').copy()
    #duplicados = sorted_books[sorted_books.duplicated(subset=['url'], keep=False)]

    avg_rating_all_books = books_wo_duplicates['avg_rating'].mean()
    min_trustable_votes = books_wo_duplicates['num_ratings'].quantile(0.25)

    #q_books = books_wo_duplicates.copy().loc[books_wo_duplicates['num_ratings'] >= min_trustable_votes]
    #shape = q_books.shape

    #shape1 = books_wo_duplicates.shape
    #print(shape)
    #print(shape1)

    books_wo_duplicates['weighted_score'] = books_wo_duplicates.apply(weighted_rating, axis=1, args=(min_trustable_votes, avg_rating_all_books))

    books_final = books_wo_duplicates.sort_values(by='weighted_score', ascending=False)
    books_final = books_final.reset_index(drop=True)

    books_final['description_clean'] = books_final['description'].apply(clean_description)
        
    books_final['metadata'] = (
        books_final['author'].apply(normalize_author) + ' ' +
        books_final['genres'].apply(normalize_genres) + ' ' +
        books_final['pages'].apply(normalize_pages)
    )
    return books_final