import pandas as pd
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from rapidfuzz import process, utils, fuzz
from sklearn.metrics.pairwise import cosine_similarity


def clean_description(text):
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([^a-zA-Z\s])', r' \1 ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    text = text.lower()
    return " ".join(text.split())


books = pd.read_json('dataset_4k.json')

books_wo_duplicates = books.sort_values(by='num_ratings', ascending=False).drop_duplicates(subset=['title', 'author'], keep='first').copy()
#duplicados = sorted_books[sorted_books.duplicated(subset=['url'], keep=False)]

avg_rating_all_books = books_wo_duplicates['avg_rating'].mean()
min_trustable_votes = books_wo_duplicates['num_ratings'].quantile(0.25)

#q_books = books_wo_duplicates.copy().loc[books_wo_duplicates['num_ratings'] >= min_trustable_votes]
#shape = q_books.shape

#shape1 = books_wo_duplicates.shape
#print(shape)
#print(shape1)
def weighted_rating(book, min_trustable_votes, avg_rating_all_books):
    v = book['num_ratings']
    R = book['avg_rating']
    return (v/(v+min_trustable_votes) * R) + (min_trustable_votes/(min_trustable_votes+v) * avg_rating_all_books)

books_wo_duplicates['weighted_score'] = books_wo_duplicates.apply(
    weighted_rating, 
    axis=1, 
    args=(min_trustable_votes, avg_rating_all_books)
)

books_final = books_wo_duplicates.sort_values(by='weighted_score', ascending=False)
books_final = books_final.reset_index(drop=True)

books_final['description_clean'] = books_final['description'].apply(clean_description)

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
    
books_final['metadata'] = (
    books_final['author'].apply(normalize_author) + ' ' +
    books_final['genres'].apply(normalize_genres) + ' ' +
    books_final['pages'].apply(normalize_pages)
)
tfidf = TfidfVectorizer(stop_words='english', min_df=5, max_df=0.8)
tfidf_meta = TfidfVectorizer(stop_words='english', min_df=1)
#books_final['description_clean'] = books_final['description_clean'].fillna('')

tfidf_matrix = tfidf.fit_transform(books_final['description_clean'])
tfidf_matrix_meta = tfidf_meta.fit_transform(books_final['metadata'])

tfidf_matrix.shape
tfidf_matrix_meta.shape

#values = tfidf.get_feature_names_out()[3000:3050]
#print(values)
#this helps us get the similarities between the books, based on the words they use in the descriptions
#cosine similarity, useful formula for this step, wikipedia page is very good
cosine_sim_desc = linear_kernel(tfidf_matrix, tfidf_matrix)
cosine_sim_meta = linear_kernel(tfidf_matrix_meta, tfidf_matrix_meta)

peso_desc = 0.7
peso_meta = 0.3
cosine_final = peso_desc * cosine_sim_desc + peso_meta * cosine_sim_meta
#with the title we can identify the index of a book

indices = pd.Series(books_final.index, index=books_final['title']).drop_duplicates()

books_final.to_csv('books_scored.csv', index=False, encoding='utf-8-sig')
STOPWORDS = {
    "the", "of", "and", "to", "in", "a", "an", "for", "on", "with", "book"
}
def has_token_overlap(a, b, min_common=2):
    tokens_a = {t for t in a.lower().split() if t not in STOPWORDS and not t.isdigit()}
    tokens_b = {t for t in b.lower().split() if t not in STOPWORDS and not t.isdigit()}
    return len(tokens_a & tokens_b) >= min_common

def user_based_recommendation(file_path):
    try:
        user_books_csv = pd.read_csv(file_path, on_bad_lines='skip')
        user_books = user_books_csv[['title', 'my rating']]

        user_books = user_books.merge(books_final.reset_index(), on='title')

        user_vector = np.zeros(tfidf_matrix.shape[1])
        user_desc_vector = np.zeros(tfidf_matrix.shape[1])

        user_meta_vector = np.zeros(
            tfidf_matrix_meta.shape[1]
        )

        for _, row in user_books.iterrows():
            book_idx = row['index'] 
            rating = row['my_rating']

            weight = rating / 5  
            user_desc_vector += (tfidf_matrix[book_idx].toarray()[0] * weight)

            user_meta_vector += (
                tfidf_matrix_meta[book_idx].toarray()[0]
                * weight
            )
        #cambiamos la shape asi cosine la toma 
        similarity_desc = cosine_similarity(user_desc_vector.reshape(1, -1), tfidf_matrix)

        similarity_meta = cosine_similarity(
            user_meta_vector.reshape(1, -1),
            tfidf_matrix_meta
        )
        similarity = (0.6 * similarity_desc + 0.4 * similarity_meta)
        scores = list(enumerate(similarity[0]))

        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        top_recommendations = [i for i, _ in scores[:10]]

        recommendations = books_final.loc[top_recommendations, ['title', 'author', 'weighted_score']]

    except FileNotFoundError:
        print("Error: El archivo no existe en esa ruta.")
        return None
    except Exception as e:
        print(f"Ocurrió un error leyendo el CSV: {e}")
        return None

def get_recommendations(title, cosine_sim=cosine_final):
    
    query = title.lower().strip()
    if len(query) < 3 or (query.isdigit() and len(query) < 4) or query in STOPWORDS:
        return f"'{title}' not found. Try again, be more specific."
    
    if query not in indices.index:#.str.lower
        #saga was causing trouble
        saga_matches = [
            t for t in indices.index
            if query in t.lower()
        ]

        if saga_matches:
            query = saga_matches[0]
        else:
            best_match = process.extractOne(
                query,
                indices.index,
                scorer=fuzz.partial_token_set_ratio
            )
            if not best_match:
                return f"'{title}' not found. Try again."
        
            candidate, score, _ = best_match

            min_score = 85 if len(query) >= 8 else 90
            query_tokens = {
                t for t in query.split()
                if t not in STOPWORDS and not t.isdigit()
            }
            if score >= min_score and len(query_tokens) == 1 or has_token_overlap(query, candidate, min_common=1):
                print(f"Couldn't find '{title}', using: '{candidate}'")
                query = candidate
            else:
                return f"'{title}' not found. Try again, be a little more specific."
        
            #if (len(query_tokens) == 1 and score >= 85) or (len(query_tokens) >= 2 and score >= 90 and has_token_overlap(query, candidate)): 
    try:
        idx = indices[query]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        
        candidates = pd.DataFrame(sim_scores, columns=['index', 'similarity'])
        
        candidates = candidates.merge(books_final[['weighted_score', 'avg_rating']], left_on='index', right_index=True)

        #candidates = candidates[candidates['rating'] >= 3]
        #no es necesario porque no tenemos nada de 3, pero es una posibilidad

        candidates['final_score'] = (candidates['similarity'] * candidates['weighted_score'])
        candidates = candidates.sort_values(by='final_score', ascending=False)
        final_indices = candidates['index'].head(10)

        return books_final.loc[final_indices, ['title', 'author', 'weighted_score']].reset_index(drop=True)
        #book_indices = [i[0] for i in sim_scores]
        #return books_final[['title', 'author', 'weighted_score']].iloc[book_indices].reset_index(drop=True)
    except Exception as e:
        return f"Some error occured with '{query}': {e}"

while True:
    user_input = input("\nName of the book you enjoyed or drag and drop your Goodreads Export (or just write 'exit'): ")
    user_input = user_input.replace('"', '').replace("'", "")
    if user_input.lower() == 'exit':
        break
    
    if user_input.endswith('.csv') and os.path.exists(user_input):
        print(f"Reading file: {user_input}...")
        recomendaciones = user_based_recommendation(user_input)
    else:
        recomendaciones = get_recommendations(user_input)
    
    if isinstance(recomendaciones, str):
        print(recomendaciones)
    else:
        if user_input.endswith('.csv'):
            print(f"\nBased on your library, you should try:\n")
        else:
            print(f"\nIf you liked '{user_input}', you should try:\n")
        print(recomendaciones[['title', 'author', 'weighted_score']])
#weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)

