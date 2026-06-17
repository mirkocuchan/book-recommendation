import os

from scripts.recommender import (get_recommendations, user_based_recommendation)

def main():
    try:
        while True:
            user_input = input("\nName of the book you enjoyed or drag and drop your Goodreads Export (or just write 'exit'): ")
            user_input = user_input.replace('"', '').replace("'", "")
            
            if user_input.lower() == 'exit':
                break
            
            if user_input.endswith('.csv') and os.path.exists(user_input):
                print(f"Reading file: {user_input}...")
                recomendaciones = user_based_recommendation(user_input)
            else:
                recomendaciones = get_recommendations(user_input)
            
            if recomendaciones is None:
                print("Could not generate recommendations.")
            elif isinstance(recomendaciones, str):
                print(recomendaciones)
            else:
                print(recomendaciones)
    except KeyboardInterrupt:
        print("\nGoodbye!")
    #weight_of_rating = ((votes_of_book // votes_of_book + min_trustable_votes) * book_average_score) + (min_trustable_votes // (min_trustable_votes + votes_of_book) * avg_rating_all_books)


if __name__ == "__main__":
    main()

