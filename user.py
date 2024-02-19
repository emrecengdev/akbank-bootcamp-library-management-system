import json
import datetime

class User:
    def __init__(self, user_file='users.json'):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, name, email):
        user_id = ''.join(random.choices('0123456789', k=5))
        if user_id not in self.users:
            self.users[user_id] = {'Name': name, 'Email': email, 'Borrowed Books': []}
            self.save_users()
            return user_id
        else:
            return None

    def borrow_book(self, user_id, book_id):
        if user_id in self.users:
            self.users[user_id]['Borrowed Books'].append({
                'Book ID': book_id,
                'Borrow Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Return Date': None
            })
            self.save_users()
            return True
        return False

    def return_book(self, user_id, book_id):
        if user_id in self.users:
            for book in self.users[user_id]['Borrowed Books']:
                if book['Book ID'] == book_id and book['Return Date'] is None:
                    book['Return Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_users()
                    return True
        return False
