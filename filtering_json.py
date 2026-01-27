import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from rapidfuzz import process, utils

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

tfidf = TfidfVectorizer(stop_words='english', min_df=5, max_df=0.8)
#books_final['description_clean'] = books_final['description_clean'].fillna('')

tfidf_matrix = tfidf.fit_transform(books_final['description_clean'])

tfidf_matrix.shape
#values = tfidf.get_feature_names_out()[3000:3050]
#print(values)
#this helps us get the similarities between the books, based on the words they use in the descriptions
#cosine similarity, useful formula for this step, wikipedia page is very good
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#with the title we can identify the index of a book

indices = pd.Series(books_final.index, index=books_final['title']).drop_duplicates()

#books_final.to_csv('books_scored.csv', index=False, encoding='utf-8-sig')

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = indices[title]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]

        book_indices = [i[0] for i in sim_scores]

        return books_final[['title', 'author', 'weighted_score']].iloc[book_indices].reset_index(drop=True)
    except KeyError:
        return f"Libro '{title}' no está el dataset."

while True:
    user_input = input("\nName of the book you enjoyed (or just write 'exit'): ")
    
    if user_input.lower() == 'exit':
        break
        
    recomendaciones = get_recommendations(user_input)
    
    if isinstance(recomendaciones, str):
        print(recomendaciones)
    else:
        print(f"\nIf you liked '{user_input}', you should try:\n")
        print(recomendaciones)
#weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)

