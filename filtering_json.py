import pandas as pd

books = pd.read_json('dataset_4k.json')

sorted_books = books.sort_values(by='avg_rating')

duplicados = sorted_books[sorted_books.duplicated(subset=['url'], keep=False)]
books_wo_duplicates = sorted_books.drop_duplicates(subset=['url'], keep='first')

books_wo_duplicates.to_csv('books.csv', index=False, encoding='utf-8-sig')



