from flask import Flask, redirect, url_for, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db=SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Bolg Post' + str(self.id)

all_posts = [
    # {
    #     'title': 'Post 1',
    #     'author': 'alex',
    #     'content': 'This is the content of post 1. bulabula'
    # },
    # {
    #     'title': 'Post 2',
    #     'content': 'This is the content of post 2. bulabula'
    # }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts_db():
    if request.method == 'POST':  
        post_title = request.form['title']
        post_conten = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_conten, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', posts=post)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name= user))
    else: 
        return render_template('login.html')


@app.route('/home/users/<string:name>')
def hello(name, id):
    return "Hello, " + name

@app.route('/onlyget', methods=['GET'])
def get_req():
    return "You can only get this weboage."


if __name__ == "__main__":
    app.run(debug=True)
