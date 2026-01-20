import requests
import re
from bs4 import BeautifulSoup

def is_duplicate(new_title, existing_titles):
    new_title_lower = new_title.lower().strip()
    for existing_title in existing_titles:
        existing_lower = existing_title.lower().strip()

        if new_title_lower in existing_lower or existing_lower in new_title_lower:
            return True
    return False

def is_first_volume(new_title):
    new_title_lower = new_title.lower().strip()
    pattern = r'#([2-9]|\d{2,})'
    
    if not re.search(pattern, new_title_lower):
        return True
    else:
        return False

    
def web_scrapping(user_input, max_recommendations   =10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
    is_author_search = user_input.lower().startswith("author: ")
    is_genre_search = user_input.lower().startswith("genre: ") 
    
    if is_author_search:
        query = user_input[8:].strip()
    elif is_genre_search:
        query = user_input[7:].strip()
    else:
        query = user_input.strip()
    
    if is_genre_search:
        genre_slug = query.lower().replace(" ", "-")
        url = f'https://www.goodreads.com/shelf/show/{genre_slug}'
    else:
        modified_query = query.replace(" ", "+")
        url = f'https://www.goodreads.com/search?utf8=%E2%9C%93&q={modified_query}&search_type=books'

    web_page = requests.get(url, headers=headers)
    content_of_webpage = web_page.text
    soup = BeautifulSoup(content_of_webpage, 'html.parser')
    possible_recommendations = {}

    if is_genre_search:
        for div in soup.find_all('div', class_='elementList'):
            if len(possible_recommendations) >= max_recommendations:
                break
            
            title_element = div.find('a', class_='bookTitle')
            if title_element:
                title = title_element.get_text().strip()
                
                if not is_duplicate(title, possible_recommendations.keys()) and is_first_volume(title):
                    author_element = div.find('span', itemprop='author')
                    if author_element:
                        author_name = author_element.find('span', itemprop='name')
                        if author_name:
                            author = author_name.get_text().strip()
                            possible_recommendations[title] = author
    else:
        for line in soup.find_all('tr', itemtype="http://schema.org/Book"):
            if len(possible_recommendations) >= max_recommendations:
                break

            title_element = line.find('span', itemprop='name')
            if title_element:
                title = title_element.get_text()
                
                if not is_duplicate(title, possible_recommendations.keys()) and is_first_volume(title):
                    author_element = line.find('span', itemprop='author')
                    if author_element:
                        author_name = author_element.find('span', itemprop='name') 
                        if author_name:
                            author = author_name.get_text()
                            
                            if is_author_search:
                                if query.lower() not in author.lower():
                                    continue
                            
                            possible_recommendations[title] = author
    
    return possible_recommendations