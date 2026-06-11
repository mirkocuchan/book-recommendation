import requests
import re
import json
import time
from bs4 import BeautifulSoup

def extract_rating_info(rating_text):
    rating_match = re.search(r'avg rating ([\d.]+)', rating_text)
    num_ratings_match = re.search(r'([\d,]+) ratings', rating_text)
    year_match = re.search(r'published (\d{4})', rating_text)
    
    return {
            'avg_rating': float(rating_match.group(1)) if rating_match else None,
            'num_ratings': int(num_ratings_match.group(1).replace(',', '')) if num_ratings_match else None,
            'year_published': int(year_match.group(1)) if year_match else None
    }

def scrape_book_details(book_url, headers):
    try:
        response = requests.get(book_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        description_elem = soup.find('div', {'data-testid': 'description'})
        description = description_elem.get_text(strip=True) if description_elem else None
        
        genres = []
        genres_section = soup.find('div', {'data-testid': 'genresList'})
        if genres_section:
            genre_buttons = genres_section.find_all('a', class_='Button--tag')
            genres = [btn.get_text(strip=True) for btn in genre_buttons]
        
        pages_elem = soup.find('p', {'data-testid': 'pagesFormat'})
        pages_text = pages_elem.get_text(strip=True) if pages_elem else None
        
        pages = None
        book_format = None
        if pages_text:
            pages_match = re.search(r'(\d+) pages', pages_text)
            format_match = re.search(r'pages, (.+)$', pages_text)
            pages = int(pages_match.group(1)) if pages_match else None
            book_format = format_match.group(1) if format_match else None
        
        return {
            'description': description,
            'genres': genres,
            'pages': pages,
            'format': book_format
        }
    
    except Exception as e:
        print(f"Error scraping {book_url}: {e}")
        return {
            'description': None,
            'genres': [],
            'pages': None,
            'format': None
        }

def scrape_goodreads_dataset(genre='fiction', num_books=7000):
    
    dataset = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    
    print(f"Starting scrape for {genre}...")
    url = f'https://www.goodreads.com/shelf/show/{genre}'
    
    while len(dataset) < num_books and url:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            book_divs = soup.find_all('div', class_='elementList')
            
            if not book_divs:
                break
            
            for div in book_divs:
                if len(dataset) >= num_books:
                    break
                
                title_elem = div.find('a', class_='bookTitle')
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()

                book_url = 'https://www.goodreads.com' + title_elem['href']
                
                author_elem = div.find('span', itemprop='name')
                author = author_elem.get_text().strip() if author_elem else None
                
                rating_elem = div.find('span', class_='greyText smallText')
                rating_info = extract_rating_info(rating_elem.get_text()) if rating_elem else {}
                
                book_data = {
                    'title': title,
                    'author': author,
                    'avg_rating': rating_info.get('avg_rating'),
                    'num_ratings': rating_info.get('num_ratings'),
                    'year_published': rating_info.get('year_published'),
                    'url': book_url,
                    'genre_category': genre
                }
                
                print(f"Scraping details for: {title} ({len(dataset)+1}/{num_books})")
                details = scrape_book_details(book_url, headers)
                book_data.update(details)
                time.sleep(1)  
                
                dataset.append(book_data)
            
            #next_page = soup.find('a', class_='next_page')
            #if not next_page:
            #    next_page = soup.find('a', rel=lambda value: value and 'next' in value)

            #if next_page and next_page.get('href'):
            #    url = 'https://www.goodreads.com' + next_page['href']
            #    print("Going to next page:", url)
            #    time.sleep(2)   
            #else:
            #    print("No next page link found — finishing genre:", genre)
            #    break
        
        except Exception as e:
            print(f"Error on page: {e}")
            time.sleep(5)
            continue
    return dataset

def save_dataset(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

def merge_json_files(file1, file2, output_file):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
        
    combined = data1 + data2
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(combined, f_out, indent=2, ensure_ascii=False)


