import pandas as pd

books = pd.read_json('dataset_4k.json')

sorted_books = books.sort_values(by='avg_rating')

duplicados = sorted_books[sorted_books.duplicated(subset=['url'], keep=False)]
books_wo_duplicates = sorted_books.drop_duplicates(subset=['url'], keep='first')

books_wo_duplicates.to_csv('books.csv', index=False, encoding='utf-8-sig')


avg_rating_all_books = books_wo_duplicates['avg_rating'].mean()
min_trustable_votes = books_wo_duplicates['num_ratings'].quantile(0.25)

#q_books = books_wo_duplicates.copy().loc[books_wo_duplicates['num_ratings'] >= min_trustable_votes]
#shape = q_books.shape

#shape1 = books_wo_duplicates.shape
#print(shape)
#print(shape1)

print(min_trustable_votes)
#weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)

