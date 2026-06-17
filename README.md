# Book Recommendation Engine
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Machine Learning](https://img.shields.io/badge/ML-Content%20Based%20Filtering-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF-yellow)
![Status](https://img.shields.io/badge/Project-Complete-success)

A content-based book recommendation engine built with Python, TF-IDF vectorization, and Goodreads data.

## Overview

Book Recommendation Engine is a command-line application that helps readers discover new books based on their interests.

The project analyzes book descriptions, metadata, ratings, and popularity metrics to generate recommendations using content-based filtering techniques. Users can either search using a book they enjoyed or upload a Goodreads export to receive personalized recommendations based on their reading history.

Rather than relying on collaborative filtering or external APIs, the system focuses on content similarity and feature engineering, making it fully self-contained and easy to run locally.

---

## Features

### Content-Based Recommendations

* Recommend books from a title the user enjoyed
* Description similarity using TF-IDF
* Metadata similarity using TF-IDF
* Combined weighted similarity scoring
* Popularity-adjusted recommendation ranking

### Personalized Recommendations

* Goodreads CSV import support
* User profile generation from ratings
* Preference vector construction
* Personalized recommendations based on reading history
* Weighted recommendations using user ratings

### Search & Matching

* Fuzzy title matching with RapidFuzz
* Partial title search support
* Typo tolerance
* Saga and series title detection
* Query validation and filtering

### Data Processing

* Dataset cleaning and preprocessing
* Duplicate book removal
* Metadata enrichment
* Rating-based book scoring
* Feature engineering pipeline

---

## Why This Project Matters

This project demonstrates several machine learning and software engineering concepts commonly used in recommendation systems:

* Content-based filtering
* Natural Language Processing (NLP)
* TF-IDF vectorization
* Cosine similarity
* Data preprocessing and cleaning
* Feature engineering
* Recommendation ranking strategies
* User preference modeling
* Command-line application development

One particularly interesting challenge was combining multiple recommendation signals into a single ranking system.

The final recommendation score combines:

* Description similarity
* Metadata similarity
* Book quality score
* Popularity metrics

This approach helps prevent low-quality books from dominating recommendations while still preserving content relevance.

The Goodreads recommendation workflow adds an additional personalization layer by creating a weighted user profile from previously rated books and comparing it against the entire catalog.

---

## Architecture

The project follows a modular architecture that separates dataset processing, recommendation logic, scoring, and user interaction.

```text
User Input
↓
CLI Interface
↓
Recommendation Engine
↓
Similarity Calculation
↓
Processed Dataset
```
### CLI Layer

Responsible for:

* Receiving user input
* Detecting title searches or CSV imports
* Displaying recommendations

### Recommendation Layer

Responsible for:

* Building TF-IDF representations
* Computing similarity matrices
* Generating recommendation rankings
* Handling fuzzy matching

### Dataset Layer

Responsible for:

* Cleaning raw data
* Creating metadata features
* Computing book quality scores
* Preparing recommendation-ready datasets

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* RapidFuzz
* TF-IDF Vectorization
* Cosine Similarity

---

## Installation

### Prerequisites

Install:

* Python 3.10+
* pip

### Clone the Repository

```bash
git clone https://github.com/yourusername/book-recommendation.git
cd book-recommendation
```

### Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

From the project root:

```bash
python -m src.main
```

The application will prompt:

```text
Name of the book you enjoyed or drag and drop your Goodreads Export (or just write 'exit'):
```

---

## Usage

### Option 1: Search by Book Title

Type the name of a book you enjoyed:

```text
Dune
```

The system will analyze its content and recommend similar books.

---

### Option 2: Goodreads Personalized Recommendations

Export your Goodreads library as CSV.

Then drag and drop the CSV file into the terminal:

```text
C:\Users\YourName\Downloads\goodreads_library_export.csv
```

The recommender will:

1. Read your ratings
2. Build a user preference profile
3. Compute content similarity
4. Return personalized recommendations

---

## Example Workflow

### Book-Based Recommendation

```text
Name of the book you enjoyed:
The Hobbit
```

Output:

```text
If you liked 'The Hobbit', you should try:

The Fellowship of the Ring
The Name of the Wind
The Eye of the World
...
```

### Goodreads-Based Recommendation

```text
Name of the book you enjoyed or drag and drop your Goodreads Export:

goodreads_library_export.csv
```

Output:

```text
Based on your library, you should try:

Hyperion
Mistborn
Project Hail Mary
...
```

---

## Project Structure

```text
book-recommendation/
│
├── scripts/
│   ├── dataset_builder.py
│   ├── dataset_preprocessing.py
│   ├── recommender.py
│   ├── scoring.py
│   ├── web_scrapping.py
│   └── utils/
│       ├── file_utils.py
│       └── text_utils.py
│
├── src/
│   └── main.py
│
├── .gitignore
├── main.sh
└── requirements.txt
```

---

## License

This project is open source and available under the MIT License.
