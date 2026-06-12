from scripts.web_scrapping import scrape_goodreads_dataset
from scripts.utils.file_utils import merge_json_files

def build_dataset():
    scrape_goodreads_dataset("fiction", num_books=3000)
    scrape_goodreads_dataset("non-fiction", num_books=1000)

    merge_json_files(
        "goodreads_fiction_final.json",
        "goodreads_non-fiction_final.json",
        "dataset_4k.json",
    )