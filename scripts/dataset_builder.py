from scripts.web_scrapping import scrape_goodreads_dataset
from scripts.utils.file_utils import merge_json_files
import argparse

def build_dataset(genre, books):
    scrape_goodreads_dataset(genre, num_books=books)

def build_default_dataset():
    scrape_goodreads_dataset("fiction", num_books=3000)
    scrape_goodreads_dataset("non-fiction", num_books=1000)

    merge_json_files("goodreads_fiction_final.json", "goodreads_non-fiction_final.json", "dataset.json",)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--genre", choices=["fiction", "non-fiction"], default="fiction")

    parser.add_argument("--books", type=int, default=1000)

    args = parser.parse_args()

    build_dataset(genre=args.genre, books=args.books)