import os
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.debug("Configuring database...")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.debug("Initializing SQLAlchemy...")
db = SQLAlchemy(app)

logging.debug("Defining Book model...")
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {'id': book.id, 'title': book.title, 'author': book.author, 'is_available': book.is_available}
        for book in books
    ])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book_status(book_id):
    book = Book.query.get_or_404(book_id)
    book.is_available = not book.is_available
    db.session.commit()
    return jsonify({'message': 'Book status updated successfully'})

if __name__ == '__main__':
    logging.debug("Creating database tables...")
    with app.app_context():
        db.create_all()
    logging.debug("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
