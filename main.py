from web_scrapping_dataset import scrape_goodreads_dataset, save_dataset, merge_json_files

def main():
    #print("Welcome! Describe the book you want.")
    #print("Please, if you want to search by author start your search with 'Author: '")
    #print("Please, if you want to search by genre start your search with 'Genre: '")
    #print("CC, write whatever you want")


    #user_input = (input(""))
    #res = web_scrapping(user_input)
    #print(res)
    fiction_books = scrape_goodreads_dataset("fiction", num_books=7000)
    save_dataset(fiction_books, 'goodreads_fiction.json')

    nonfiction_books = scrape_goodreads_dataset("nonfiction", num_books=3000)
    save_dataset(nonfiction_books, 'goodreads_nonfiction.json')

    
    merge_json_files('goodreads_fiction.json', 'goodreads_nonfiction.json', 'goodreads_full_dataset.json')

if __name__ == "__main__":
        main()
