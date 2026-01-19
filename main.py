from web_scrapping import web_scrapping

def main():
    print("Welcome! Describe the book you want.")
    
    user_input = (input(""))
    res = web_scrapping(user_input)
    print(res)


if __name__ == "__main__":
        main()
