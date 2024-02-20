import sys
import pandas as pd
import random
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, \
    QMessageBox, QTextEdit, QToolBar
from PyQt5.QtGui import QIcon


class Library:
    def __init__(self):
        self.books_file = "books.txt"
        self.load_books()

    def load_books(self):
        try:
            self.books_df = pd.read_csv(self.books_file, header=0)
        except FileNotFoundError:
            self.books_df = pd.DataFrame(
                columns=['ID', 'Title', 'Author', 'Publish Date', 'Page Count', 'Genre', 'Added Date'])

    # Dosyayı kaydetmek için açıkça bir metod kullanın
    def save_books_to_file(self):
        self.books_df.to_csv(self.books_file, index=False)

    def add_book(self, title, author, publish_date, page_count, genre):
        new_id = ''.join(random.choice('0123456789') for _ in range(5))
        today = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([[new_id, title, author, publish_date, page_count, genre, today]],
                               columns=['ID', 'Title', 'Author', 'Publish Date', 'Page Count', 'Genre', 'Added Date'])
        self.books_df = pd.concat([self.books_df, new_row], ignore_index=True)
        self.save_books_to_file()  # Kitap ekledikten sonra dosyayı kaydedin

    def remove_book(self, title):
        self.books_df = self.books_df[self.books_df['Title'] != title]
        self.save_books_to_file()

    def list_books(self):
        return self.books_df.to_string(index=False)


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.setWindowTitle('Library Management System')
        self.setGeometry(100, 100, 600, 400)
        self.initUI()
        self.menu_stack = []

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()

        self.librarianButton = QPushButton('Görevli Girişi')
        self.memberButton = QPushButton('Üye Girişi')
        self.librarianButton.clicked.connect(self.librarianMenu)
        self.memberButton.clicked.connect(self.memberMenu)

        self.layout.addWidget(self.librarianButton)
        self.layout.addWidget(self.memberButton)

        self.centralWidget.setLayout(self.layout)

        # Ok tuşları için toolbar ekle
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Ok tuşları ekle
        self.backButton = QPushButton('←')
        self.forwardButton = QPushButton('→')
        self.toolbar.addWidget(self.backButton)
        self.toolbar.addWidget(self.forwardButton)

        # Ok tuşlarına fonksiyonlar bağla
        self.backButton.clicked.connect(self.goBack)
        self.forwardButton.clicked.connect(self.goForward)

    def goToMenu(self, menu_func):
        self.clearLayout(self.layout)
        menu_func()
        self.menu_stack.append(menu_func)
        print("Went to menu:", menu_func.__name__)
        print("Menu stack:", [menu.__name__ for menu in self.menu_stack])

    def goBack(self):
        if len(self.menu_stack) > 1:
            prev_menu = self.menu_stack.pop()
            prev_menu = self.menu_stack[-1] if self.menu_stack else None
            if prev_menu:
                self.clearLayout(self.layout)
                prev_menu()
                print("Went back to:", prev_menu.__name__)
                print("Menu stack:", [menu.__name__ for menu in self.menu_stack])

    def goForward(self):
        if len(self.menu_stack) > 1:
            current_menu_index = self.menu_stack.index(self.menu_stack[-1])
            if current_menu_index > 0:
                next_menu_index = current_menu_index - 1
                next_menu = self.menu_stack[next_menu_index]
                self.goToMenu(next_menu)
                print("Went forward to:", next_menu.__name__)
            else:
                print("Cannot go forward.")

    def librarianMenu(self):
        self.clearLayout(self.layout)
        self.addBookButton = QPushButton('Kitap Ekle')
        self.removeBookButton = QPushButton('Kitap Sil')
        self.listBooksButton = QPushButton('Kitapları Listele')

        self.addBookButton.clicked.connect(lambda: self.goToMenu(self.addBook))
        self.removeBookButton.clicked.connect(lambda: self.goToMenu(self.removeBookPrompt))
        self.listBooksButton.clicked.connect(self.listBooks)

        self.layout.addWidget(self.addBookButton)
        self.layout.addWidget(self.removeBookButton)
        self.layout.addWidget(self.listBooksButton)

        # Görevli menüsündeyken ana menüdeki giriş butonlarını gizle
        self.librarianButton.setVisible(False)
        self.memberButton.setVisible(False)

    def memberMenu(self):
        self.clearLayout(self.layout)
        self.layout.addWidget(QLabel('Üye işlevselliği henüz eklenmedi.'))

    def addBook(self):
        self.clearLayout(self.layout)
        self.titleInput = QLineEdit()
        self.authorInput = QLineEdit()
        self.publishDateInput = QLineEdit()
        self.pageCountInput = QLineEdit()
        self.genreInput = QLineEdit()
        self.submitButton = QPushButton('Kitap Ekle')

        self.submitButton.clicked.connect(self.submitBook)

        self.layout.addWidget(QLabel('Başlık:'))
        self.layout.addWidget(self.titleInput)
        self.layout.addWidget(QLabel('Yazar:'))
        self.layout.addWidget(self.authorInput)
        self.layout.addWidget(QLabel('Yayın Tarihi:'))
        self.layout.addWidget(self.publishDateInput)
        self.layout.addWidget(QLabel('Sayfa Sayısı:'))
        self.layout.addWidget(self.pageCountInput)
        self.layout.addWidget(QLabel('Tür:'))
        self.layout.addWidget(self.genreInput)
        self.layout.addWidget(self.submitButton)

    def submitBook(self):
        title = self.titleInput.text()
        author = self.authorInput.text()
        publish_date = self.publishDateInput.text()
        page_count = self.pageCountInput.text()
        genre = self.genreInput.text()
        self.library.add_book(title, author, publish_date, page_count, genre)
        QMessageBox.information(self, 'Kitap Eklendi', 'Kitap başarıyla eklendi!')
        self.goBack()

    def removeBookPrompt(self):
        self.clearLayout(self.layout)
        self.titleInput = QLineEdit()
        self.submitButton = QPushButton('Kitap Sil')

        self.submitButton.clicked.connect(self.submitRemoveBook)

        self.layout.addWidget(QLabel('Silinecek Kitabın Başlığı:'))
        self.layout.addWidget(self.titleInput)
        self.layout.addWidget(self.submitButton)

    def submitRemoveBook(self):
        title = self.titleInput.text()
        self.library.remove_book(title)
        QMessageBox.information(self, 'Kitap Silindi', 'Kitap başarıyla silindi!')
        self.goBack()

    def listBooks(self):
        self.clearLayout(self.layout)
        books_list = QTextEdit()
        books_list.setPlainText(self.library.list_books())
        books_list.setReadOnly(True)
        self.layout.addWidget(books_list)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = LibraryApp()
    mainWin.show()
    sys.exit(app.exec_())
