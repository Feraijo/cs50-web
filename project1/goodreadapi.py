import requests


if __name__ == '__main__':
    res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                        params={"key": "kUm8d7pDXxEwlsr7XrGA0g", "isbns": "9781632168146"})
    print(res.json())
