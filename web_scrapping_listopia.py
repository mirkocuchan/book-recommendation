import requests
import re
import json
import time
from bs4 import BeautifulSoup

def extract_rating_info(rating_text):
    # Formato en listas: "4.12 avg rating — 1,234,567 ratings"
    rating_match = re.search(r'([\d.]+)\s+avg rating', rating_text)
    num_ratings_match = re.search(r'([\d,]+)\s+ratings', rating_text)
    return {
        'avg_rating': float(rating_match.group(1)) if rating_match else None,
        'num_ratings': int(num_ratings_match.group(1).replace(',', '')) if num_ratings_match else None
    }

def scrape_book_details(book_url, headers):
    try:
        response = requests.get(book_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Descripción
        description_elem = soup.find('div', {'data-testid': 'description'})
        description = description_elem.get_text(strip=True) if description_elem else None
        
        # Géneros
        genres = []
        genres_section = soup.find('div', {'data-testid': 'genresList'})
        if genres_section:
            genre_buttons = genres_section.find_all('a', class_='Button--tag')
            genres = list(set([btn.get_text(strip=True) for btn in genre_buttons]))
        
        # Páginas y Formato
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
        return {'description': None, 'genres': [], 'pages': None, 'format': None}

def scrape_goodreads_dataset(genre_type='fiction', num_books=7000):
    dataset = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    list_mapping = {
        'fiction': 'https://www.goodreads.com/list/show/1.Best_Books_Ever',
        'non-fiction': 'https://www.goodreads.com/list/show/134.Best_Non_Fiction_No_Biographies_'
    }
    
    base_url = list_mapping.get(genre_type)
    page = 1
    seen_urls = set()
    
    print(f"\n Iniciando extracción de {genre_type.upper()} via Listopia...")

    while len(dataset) < num_books:
        url = f'{base_url}?page={page}'
        print(f"\n--- Leyendo Página {page} ---")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Error de conexión: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            # Las listas usan filas de tabla (tr)
            book_rows = soup.find_all('tr', itemtype='http://schema.org/Book')
            
            if not book_rows:
                print("No se encontraron más libros.")
                break
            
            for row in book_rows:
                if len(dataset) >= num_books: break
                
                title_elem = row.find('a', class_='bookTitle')
                book_url = 'https://www.goodreads.com' + title_elem['href']
                
                if book_url in seen_urls: continue
                
                title = title_elem.get_text().strip()
                author = row.find('a', class_='authorName').get_text().strip()
                
                # Info de rating
                rating_text = row.find('span', class_='minirating').get_text()
                rating_info = extract_rating_info(rating_text)
                
                print(f"[{len(dataset)+1}/{num_books}] Procesando: {title[:40]}")
                
                # Detalles profundos
                details = scrape_book_details(book_url, headers)
                
                book_data = {
                    'title': title,
                    'author': author,
                    'avg_rating': rating_info['avg_rating'],
                    'num_ratings': rating_info['num_ratings'],
                    'url': book_url,
                    'genre_category': genre_type
                }
                book_data.update(details)
                
                dataset.append(book_data)
                seen_urls.add(book_url)
                
                time.sleep(1.1) # Respeto al servidor
                
            # Guardado parcial cada 100 libros
            if len(dataset) % 100 == 0:
                save_dataset(dataset, f'goodreads_{genre_type}_partial.json')

            page += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"Error en página {page}: {e}")
            break

    save_dataset(dataset, f'goodreads_{genre_type}_final.json')
    return dataset

def save_dataset(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

def merge_json_files(file1, file2, output_file):
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            d1, d2 = json.load(f1), json.load(f2)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(d1 + d2, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Dataset total creado: {output_file}")
    except Exception as e:
        print(f"Error al unir: {e}")