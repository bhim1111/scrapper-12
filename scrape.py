import requests

from bs4 import BeautifulSoup
import json
import sqlite3
import csv

#git init
#git status => if you want to check what are the status of file
#git add .
#git commit -m "bhim timsina"
#create repository in github
#copy past git code from github



#1 change the code
#2 git add .
#3 git commit -m "your message"
#4 git push



# URL of the website to scrape
url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code {response.status_code}")
        return []

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    all_books = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find("p", class_="price_color").text
        
        currency = price_text[0]       # £
        price = float(price_text[1:])  # 51.77
        
        print(title, currency, price)

        all_books.append({
            "title": title,
            "currency": currency,
            "price": price
        })

    return all_books


def save_to_json(books):
    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)
    print("✔ JSON saved successfully!")


def save_to_csv(books):
    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "currency", "price"])
        writer.writeheader()
        writer.writerows(books)
    print("✔ CSV saved successfully!")


def create_table():
   
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            currency TEXT,
            price REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✔ Database and table created successfully!")


def insert_book(title, currency, price):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, currency, price) VALUES (?, ?, ?)",
        (title, currency, price)
    )

    conn.commit()
    conn.close()


def main():
    books = scrape_books(url)   # ✅ FIXED

    save_to_csv(books)
    save_to_json(books)
    create_table()
    for book in books:
        insert_book(book["title"], book["currency"], book["price"])
    print("✔ All books inserted into database!")


main()
