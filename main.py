from web_scrapping_dataset import scrape_goodreads_dataset, save_dataset, merge_json_files
from web_scrapping_listopia import scrape_goodreads_dataset, save_dataset, merge_json_files
import json

def main():
    

    scrape_goodreads_dataset("fiction", num_books=3000)
    scrape_goodreads_dataset("non-fiction", num_books=1000)
    
    merge_json_files('goodreads_fiction_final.json', 'goodreads_non-fiction_final.json', 'dataset_4k.json')

if __name__ == "__main__":
    main()
