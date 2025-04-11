import streamlit as st
import json
import os

# Define the data file at the top level
data_file = 'library.json'

# Ensure the library file exists and is valid
def ensure_library_file():
    if not os.path.exists(data_file):
        with open(data_file, 'w') as file:
            json.dump([], file)  # Write an empty list as the initial content

# Load & Save library data
def load_library():
    ensure_library_file()  # Call this to make sure file exists
    try:
        with open(data_file, 'r') as file:
            library = json.load(file)
            # Ensure each book has all required fields with defaults
            for book in library:
                if 'title' not in book:
                    book['title'] = 'Unknown'
                if 'author' not in book:
                    book['author'] = 'Unknown'
                if 'year' not in book:
                    book['year'] = 'Unknown'
                if 'genre' not in book:
                    book['genre'] = 'Unknown'
                if 'read' not in book:
                    book['read'] = False
            return library
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Return empty list if file is corrupted or doesn't exist
    
def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)  # Added indent for better readability

def add_book(library):
    title = st.text_input('Enter the title of the book:') 
    author = st.text_input('Enter the author of the book:')
    year = st.text_input('Enter the year of the book:')
    genre = st.text_input('Enter the genre of the book:')
    read = st.radio("Have you read the book?", ("Yes", "No")) == "Yes"

    if st.button("Add Book"):
        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'genre': genre,
            'read': read
        }

        library.append(new_book)
        save_library(library)
        st.success(f'Book "{title}" added successfully.')

def remove_book(library):
    title = st.text_input("Enter the title of the book to remove:").lower()
    if st.button("Remove Book"):
        initial_length = len(library)
        library[:] = [book for book in library if book.get('title', '').lower() != title]
        if len(library) < initial_length:
            save_library(library)
            st.success(f'Book "{title}" removed successfully.')
        else:
            st.error(f'Book "{title}" not found in the library.')

def search_library(library):
    search_by = st.radio("Search by:", ["Title", "Author"]).lower()
    search_term = st.text_input(f"Enter the {search_by} to search for:").lower()
    
    if st.button("Search"):
        results = []
        for book in library:
            # Safely access all fields
            if search_term in book.get(search_by, '').lower():
                results.append(book)
        
        if results:
            st.write("\nSearch Results:")
            for book in results:
                status = "read" if book.get('read', False) else "unread"
                st.write(f"{book.get('title', 'Unknown')} by {book.get('author', 'Unknown')} "
                          f"({book.get('year', 'Unknown')}) - {book.get('genre', 'Unknown')} - {status}")
        else:
            st.write(f"\nNo books found matching '{search_term}' in the {search_by} field.")

def display_all_books(library):
    if library:
        st.write("\nAll Books in Library:")
        for book in library:
            status = "Read" if book.get('read', False) else "Unread"
            st.write(f"{book.get('title', 'Unknown')} by {book.get('author', 'Unknown')} "
                      f"({book.get('year', 'Unknown')}) - {book.get('genre', 'Unknown')} - {status}")
    else:
        st.write("The library is empty.")

def display_statistics(library):
    total_books = len(library)
    read_books = len([book for book in library if book.get('read', False)])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write("\nLibrary Statistics:")
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Percentage read: {percentage_read:.1f}%")

def main():
    st.title("Library Management System")
    library = load_library()
    
    menu = ["Add a book", "Remove a book", "Search the library", 
            "Display all books", "Display statistics", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a book":
        add_book(library)
    elif choice == "Remove a book":
        remove_book(library)
    elif choice == "Search the library":
        search_library(library)
    elif choice == "Display all books":
        display_all_books(library)
    elif choice == "Display statistics":
        display_statistics(library)
    elif choice == "Exit":
        st.write("Goodbye!")
        st.stop()

if __name__ == '__main__':
    main()