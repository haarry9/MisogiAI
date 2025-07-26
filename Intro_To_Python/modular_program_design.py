def add_book(lib: list, title: str, author: str):
    lib.append({"title": title, "author": author})
    print(f"Book {title} by {author} added to the library.")

def search_book(library: list, search_title: str):
    for book in library:
        if book["title"].lower() == search_title.lower():
            print(f"Found: {book['title']} by {book['author']}")
            return
    print("Book not found.")

def display_books(library: list):
    if not library:
        print("The library is empty.")
    else:
        print("\nLibrary Inventory:")
        for idx, book in enumerate(library, start=1):
            print(f"{idx}. {book['title']} by {book['author']}")

def main():
    library = []   # Inventory list
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Display All Books")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            add_book(library, title, author)
        elif choice == "2":
            search_title = input("Enter title to search: ")
            search_book(library, search_title)
        elif choice == "3":
            display_books(library)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()