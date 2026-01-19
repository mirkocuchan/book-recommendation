import requests
from bs4 import BeautifulSoup

def is_duplicate(new_title, existing_titles):
    new_title_lower = new_title.lower().strip()
    for existing_title in existing_titles:
        existing_lower = existing_title.lower().strip()

        if new_title_lower in existing_lower or existing_lower in new_title_lower:
            return True
    return False

def web_scrapping(user_input, max_recommendations   =10):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    if len(user_input) > 1:
        modified_user_input = user_input.replace(" ", "+")
        web_page = requests.get(f'https://www.goodreads.com/search?utf8=%E2%9C%93&q={modified_user_input}&search_type=books', headers=headers)
    
    else:    
        web_page = requests.get(f'https://www.goodreads.com/search?utf8=%E2%9C%93&q={user_input}&search_type=books', headers=headers)

    content_of_webpage = web_page.text

    soup = BeautifulSoup(content_of_webpage, 'html.parser')

    possible_recommendations = {}
    for line in soup.find_all('tr', itemtype="http://schema.org/Book"):
        if len(possible_recommendations) >= max_recommendations:
            break

        title_element = line.find('span', itemprop='name')
        if title_element:
            title = title_element.get_text()
            if not is_duplicate(title, possible_recommendations.keys()):
                author_element = line.find('span', itemprop='author')
                if author_element:
                    author_name = author_element.find('span', itemprop='name') 
                    if author_name:
                        author = author_name.get_text()
                        possible_recommendations[title] = author
    return possible_recommendations