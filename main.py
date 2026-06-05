from web_scrapping_dataset import scrape_goodreads_dataset, save_dataset, merge_json_files
from web_scrapping_listopia import scrape_goodreads_dataset, save_dataset, merge_json_files
import json

def main():
    #print("Welcome! Describe the book you want.")
    #print("Please, if you want to search by author start your search with 'Author: '")
    #print("Please, if you want to search by genre start your search with 'Genre: '")
    #print("CC, write whatever you want")


    #user_input = (input(""))
    #res = web_scrapping(user_input)
    #print(res)
#    genres = [
#        "fantasy",
#        "fiction",
#        "non-fiction",
#        "romance",
#        "mystery",
#        "classics",
#        "horror",
#        "science-fiction",
#        "thriller",
#        "poetry",
#        "historical",
#        "philosophy",
#        "biography",
#    ]

#    all_books = []

#    for g in genres:
#        print(f"\n=== Scraping genre: {g} ===")
#        books = scrape_goodreads_dataset(genre=g, num_books=50)
#        all_books.extend(books)

#    print(f"\nTotal books scraped: {len(all_books)}")

#    with open("goodreads_multi_genres.json", "w", encoding="utf-8") as f:
#        json.dump(all_books, f, ensure_ascii=False, indent=2)

    scrape_goodreads_dataset("fiction", num_books=3000)
    scrape_goodreads_dataset("non-fiction", num_books=1000)
    
    merge_json_files('goodreads_fiction_final.json', 'goodreads_non-fiction_final.json', 'dataset_4k.json')

if __name__ == "__main__":
    main()
