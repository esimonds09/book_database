from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///my_books.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Library).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        new_book = Library(title=request.form['book_name'],
                           author=request.form['author'],
                           rating=request.form['rating'])

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')

@app.route("/edit", methods=["POST", "GET"])
def edit_rating():
    if request.method == "POST":
        book_id = request.form['id']
        new_rating = request.form['rating']
        book_to_update = Library.query.get(book_id)
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book = Library.query.get(book_id)
    return render_template("edit.html", book=book)

@app.route("/delete", methods=["POST", "GET"])
def delete():
    book_id = request.args.get('id')
    book_to_delete = Library.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)

