import json
from datetime import datetime

DATA_FILE = "library_data.json"

class Library:
    def __init__(self, name, n=0, books=None, issued_books=None):
        self.name = name
        self.number_of_books = n
        self.books = books if books else []
        self.issued_books = issued_books if issued_books else {}

    def save_data(self):
        """Save the current library state to a file."""
        with open(DATA_FILE, "w") as file:
            json.dump(libraries, file, default=lambda obj: obj.__dict__, indent=4)

    def show_books(self):
        if self.books:
            print("\nBooks available in the library:")
            for book in self.books:
                print(f"- {book.title()} (Available)")
        else:
            print("\nNo books available in the library.")

        if self.issued_books:
            print("\nIssued Books:")
            for book, details in self.issued_books.items():
                print(f"- {book.title()} (Issued by {details['borrower']} on {details['issue_date']})")

    def check_num_books(self):
        print(f"\nTotal books added: {self.number_of_books}")
        print(f"Books currently in library: {len(self.books)}")
        print(f"Books issued: {len(self.issued_books)}")
        if self.number_of_books != len(self.books) + len(self.issued_books):
            print("Error: Number of books doesn't match! Check the records.")

    def add_books(self, n, new_books):
        self.number_of_books += n
        self.books.extend(new_books)
        print(f"\n{n} book(s) added successfully.")
        self.save_data()

    def remove_books(self, books_to_remove):
        for book in books_to_remove:
            if book in self.books:
                self.books.remove(book)
                self.number_of_books -= 1
                print(f"'{book.title()}' removed from the library.")
            elif book in self.issued_books:
                print(f"'{book.title()}' is currently issued and cannot be removed.")
            else:
                print(f"'{book.title()}' not found in the library.")
        self.save_data()

    def borrow_book(self, book, borrower_name):
        if book in self.books:
            self.books.remove(book)
            self.issued_books[book] = {
                "borrower": borrower_name,
                "issue_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "return_date": None
            }
            print(f"\n'{book.title()}' issued to {borrower_name}.")
        elif book in self.issued_books:
            print(f"\n'{book.title()}' is already issued by {self.issued_books[book]['borrower']} on {self.issued_books[book]['issue_date']}.")
        else:
            print(f"\n'{book.title()}' is not available in the library.")
        self.save_data()

    def return_book(self, book):
        if book in self.issued_books:
            self.books.append(book)
            self.issued_books[book]['return_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n'{book.title()}' returned successfully. Issued by {self.issued_books[book]['borrower']} on {self.issued_books[book]['issue_date']}, returned on {self.issued_books[book]['return_date']}.")
            del self.issued_books[book]
        else:
            print(f"\n'{book.title()}' was not issued, cannot be returned.")
        self.save_data()

def load_data():
    """Load library data from a file."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return {name: Library(name, d['number_of_books'], d['books'], d['issued_books']) for name, d in data.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def library_menu(lib):
    while True:
        print("\nLibrary Menu")
        choice = int(input("1. Show Books\n2. Check Book Count\n3. Add Books\n4. Remove Books\n5. Borrow a Book\n6. Return a Book\n7. Go Back\nEnter your choice: "))
        if choice == 1:
            lib.show_books()
        elif choice == 2:
            lib.check_num_books()
        elif choice == 3:
            n = int(input("\nEnter number of books to add: "))
            books = input("Enter book titles (comma-separated): ").lower().split(", ")
            lib.add_books(n, books)
        elif choice == 4:
            books = input("\nEnter book titles to remove (comma-separated): ").lower().split(", ")
            lib.remove_books(books)
        elif choice == 5:
            book = input("\nEnter the book title to borrow: ").lower()
            borrower = input("Enter your name: ")
            lib.borrow_book(book, borrower)
        elif choice == 6:
            book = input("\nEnter the book title to return: ").lower()
            lib.return_book(book)
        elif choice == 7:
            break
        else:
            print("\nInvalid choice! Try again.")

libraries = load_data()

while True:
    print("\nMain Menu")
    action = input("1. Choose Library\n2. Create Library\n3. Exit\nEnter your choice: ")
    
    if action == "2":
        lib_name = input("\nEnter library name: ")
        num_books = int(input("Enter initial number of books: "))
        book_list = input("Enter book titles (comma-separated): ").lower().split(",")
        libraries[lib_name] = Library(lib_name, num_books, book_list)
        libraries[lib_name].save_data()
        print(f"\nLibrary '{lib_name}' created successfully.")
    elif action == "1":
        lib_name = input("\nEnter library name: ")
        if lib_name in libraries:
            library_menu(libraries[lib_name])
        else:
            print("\nLibrary not found.")
    elif action == "3":
        print("\nThank you for using the Library Management System.")
        break
    else:
        print("\nInvalid choice! Please enter a valid option.")