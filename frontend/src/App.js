// frontend/src/App.js
import React, { useState, useEffect } from 'react';

function App() {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ title: '', author: '' });

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    const response = await fetch('http://localhost:5000/books');
    const data = await response.json();
    setBooks(data);
  };

  const addBook = async (e) => {
    e.preventDefault();
    await fetch('http://localhost:5000/books', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newBook),
    });
    setNewBook({ title: '', author: '' });
    fetchBooks();
  };

  const updateBookStatus = async (id) => {
    await fetch(`http://localhost:5000/books/${id}`, { method: 'PUT' });
    fetchBooks();
  };

  return (
    <div>
      <h1>Library Management</h1>
      <form onSubmit={addBook}>
        <input
          type="text"
          placeholder="Title"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Author"
          value={newBook.author}
          onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
        />
        <button type="submit">Add Book</button>
      </form>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            {book.title} by {book.author} - 
            <button onClick={() => updateBookStatus(book.id)}>
              {book.is_available ? 'Take' : 'Return'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;