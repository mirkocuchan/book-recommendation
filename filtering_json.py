import pandas as pd

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

books_final.to_csv('books_scored.csv', index=False, encoding='utf-8-sig')

print(min_trustable_votes)
#weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)

