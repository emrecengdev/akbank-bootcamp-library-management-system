from library import Library
from user import User

def add_user(user_system):
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    user_id = user_system.add_user(name, email)
    if user_id:
        print(f"User added successfully. User ID: {user_id}")
    else:
        print("User could not be added.")

def add_book(library):
    name = input("Enter book name: ")
    author = input("Enter author name: ")
    publication_date = input("Enter publication date: ")
    page_number = input("Enter page number: ")
    book_type = input("Enter book type: ")
    library.add_book(name, author, publication_date, page_number, book_type)
    print("Book added successfully.")

def remove_book(library):
    name = input("Enter the name of the book to remove: ")
    library.remove_book(name)
    print("Book removed successfully.")

def lend_book(library, user_system):
    user_id = input("Enter user ID: ")
    book_id = input("Enter book ID: ")
    library.lend_book(user_id, book_id)

def return_book(library, user_system):
    user_id = input("Enter user ID: ")
    book_id = input("Enter book ID: ")
    library.return_book(user_id, book_id)

def list_books(library):
    print(library.list_books())

def main_menu():
    library = Library()
    user_system = User()

    while True:
        print("\n*** LIBRARY MENU ***")
        print("1) List Books")
        print("2) Add Book")
        print("3) Remove Book")
        print("4) Lend a Book")
        print("5) Return a Book")
        print("6) Add User")
        print("7) Exit")
        choice = input("Please select an option: ")

        if choice == '1':
            list_books(library)
        elif choice == '2':
            add_book(library)
        elif choice == '3':
            remove_book(library)
        elif choice == '4':
            lend_book(library, user_system)
        elif choice == '5':
            return_book(library, user_system)
        elif choice == '6':
            add_user(user_system)
        elif choice == '7':
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    main_menu()
