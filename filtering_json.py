import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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

sorted_books = books.sort_values(by='num_ratings', ascending=False)

#duplicados = sorted_books[sorted_books.duplicated(subset=['url'], keep=False)]
books_wo_duplicates = sorted_books.drop_duplicates(subset=['title', 'author'], keep='first').copy()

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

books_final['description_clean'] = books_final['description'].apply(clean_description)

tfidf = TfidfVectorizer(stop_words='english', min_df=5, max_df=0.8)
books_final['description_clean'] = books_final['description_clean'].fillna('')

tfidf_matrix = tfidf.fit_transform(books_final['description_clean'])

tfidf_matrix.shape
#values = tfidf.get_feature_names_out()[3000:3050]
#print(values)
#this helps us get the similarities between the books, based on the words they use in the descriptions
#cosine similarity, useful formula for this step, wikipedia page is very good
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(books_final.index, index=books_final['title']).drop_duplicates()

books_final.to_csv('books_scored.csv', index=False, encoding='utf-8-sig')


#weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)

