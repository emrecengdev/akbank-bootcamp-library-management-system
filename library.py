import pandas as pd
import random
import datetime

class Library:
    def __init__(self, books_file='books.txt'):
        self.books_file = books_file
        self.load_books()

    def __del__(self):
        self.save_books()

    def load_books(self):
        try:
            self.books_df = pd.read_csv(self.books_file, header=None, names=['ID', 'Book Name', 'Author', 'Publication Date', 'Page Number', 'Type', 'Added Date'])
        except FileNotFoundError:
            self.books_df = pd.DataFrame(columns=['ID', 'Book Name', 'Author', 'Publication Date', 'Page Number', 'Type', 'Added Date'])

    def save_books(self):
        self.books_df.to_csv(self.books_file, index=False, header=False)

    def add_book(self, name, author, publication_date, page_number, book_type):
        book_id = ''.join(random.choices('0123456789', k=5))
        added_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.books_df = self.books_df.append({'ID': book_id, 'Book Name': name, 'Author': author, 'Publication Date': publication_date, 'Page Number': page_number, 'Type': book_type, 'Added Date': added_date}, ignore_index=True)

    def remove_book(self, name):
        self.books_df = self.books_df[self.books_df['Book Name'] != name]

    def list_books(self):
        return self.books_df[['ID', 'Book Name', 'Author', 'Publication Date', 'Page Number', 'Type', 'Added Date']].to_string(index=False)

    # Ödünç verme işlemleri ve diğer fonksiyonlar burada tanımlanacak

# library.py dosyasına eklemeler

    def lend_book(self, user_id, book_id):
        # User sınıfı kullanılarak bir kitabın ödünç verilmesi işlemi
        user = User()  # User sınıfının bir örneğini oluştur
        if user.borrow_book(user_id, book_id):
            print(f"Book {book_id} has been lent to user {user_id}.")
        else:
            print("Error: Could not lend the book.")

    def return_book(self, user_id, book_id):
        # User sınıfı kullanılarak bir kitabın iadesi işlemi
        user = User()  # User sınıfının bir örneğini oluştur
        if user.return_book(user_id, book_id):
            print(f"Book {book_id} has been returned by user {user_id}.")
        else:
            print("Error: Could not return the book.")
