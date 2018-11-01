from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:happy@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asfsfadasdfk'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods = ['POST', 'GET'])
def index():

    
    if request.method == 'POST':
        post_name = request.form['newpost']
        post_body = request.form['body']
        if len(post_name) != 0 and len(post_name) != 0:
            new_post = Blog(post_name, post_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')

        elif len(post_name) == 0 or len(post_body) == 0:
            flash('Please fill in the title', category='error')
            flash('Please fill in the body', category='info')
            return redirect('/newpost')

    return render_template('newpost.html',title='Add a new entry')

@app.route('/blog')
def blog_posts():

    blogs = Blog.query.filter_by().all()
    return render_template('blog.html',title='Build a blog', blogs=blogs)    


@app.route('/single')
def single():

    
    blogs = Blog.query.filter_by().all()
    return render_template('single.html', blogs=blogs)

if __name__ == '__main__':
    app.run()