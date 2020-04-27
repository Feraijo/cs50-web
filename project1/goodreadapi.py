import requests

__KEY__ = "kUm8d7pDXxEwlsr7XrGA0g"
__REV_COUNTS__ = 'https://www.goodreads.com/book/review_counts.json'

def get_book_data(isbn):
    res = requests.get(__REV_COUNTS__, params={"key": __KEY__, "isbns": isbn})
    if res.status_code == 404:
        return {}
    book_data = res.json()['books'][0]
    return book_data    

if __name__ == '__main__':
    i = "074349671X"
    print(get_book_data(i))
    
