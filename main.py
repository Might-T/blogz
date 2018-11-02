from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:finishit@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asfsfadasdfk'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner =owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password





def database_match(x,y):
    if x == y:
        return True
    else:
        return False
def is_proper_length(x):
    if len(x) <20 and len(x) >3:
        return True
    else:
        return False

def space_check(element):    
    if ' ' in element:
        return True
    else:
        return False

def special_char(element):
    if '@' in element and '.' in element:
        return True
    else:
        False
        
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog','single']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login ():
   
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        
        elif database_match(user,username):
            flash('Username does not exist', 'usern')


    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup ():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        if not is_proper_length(username):
            flash('User name must be 3 to 20 characters long.','user_error')
            return render_template('signup.html')     
        elif space_check(username):
            flash('Please remove space(s) from username', 'user_error') 
            return render_template('signup.html')

        if not is_proper_length(password):
            flash('Password must be 3 to 20 characters long.', 'pass_w')
            return render_template('signup.html')
        elif space_check(password):
            flash( 'Please remove space(s) from password', 'pass_w' )            
            return render_template('signup.html')
        if not is_proper_length(verify):
            flash('Verify password must be at least 3 characters long.','veri_error')
            return render_template('signup.html')  
        elif verify !=password:
            flash('Password and Verify password do not match','veri_error')  
            return render_template('signup.html')     
    
        existing_user = User.query.filter_by(username=username).first()  
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('That username already exits', 'user_error')

    return render_template('signup.html')


@app.route('/newpost', methods = ['POST', 'GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        post_name = request.form['newpost']
        post_body = request.form['body']
        if len(post_name) != 0 and len(post_name) != 0:
            new_post = Blog(post_name, post_body, owner)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/single')

        elif len(post_name) == 0 or len(post_body) == 0:
            flash('Please fill in the title', category='error')
            flash('Please fill in the body', category='info')
            return redirect('/newpost')

    return render_template('newpost.html',title='Add a new entry')

@app.route('/blog')
def blog_posts():

    blogs = Blog.query.filter_by().all()
    return render_template('blog.html',title='Build a blog', blogs=blogs)    

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/single')
def single():
    blog_id =request.args.get('id')
    blog = Blog.query.get(blog_id)
    blogs = Blog.query.filter_by().all()
    return render_template('single.html', blogs=blogs, blog=blog)

if __name__ == '__main__':
    app.run()