from web_scrapping import web_scrapping

def main():
    print("Welcome! Describe the book you want.")
    print("Please, if you want to search by author start your search with 'Author: '")
    print("Please, if you want to search by genre start your search with 'Genre: '")
    print("CC, write whatever you want")


    user_input = (input(""))
    res = web_scrapping(user_input)
    print(res)


if __name__ == "__main__":
        main()
