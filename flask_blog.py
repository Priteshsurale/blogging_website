from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#  secret key protect against modifying cookies and cross site request forgery(csrf) attacks.
app.config['SECRET_KEY'] = '0b134aeac20f8b7faa9b88a2087030f5' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# posts data
posts = [
    {
      'author': 'Pritesh Surale',
      'title': 'Blog Post 1',
      'content': 'First post content',
      'date_posted': 'April 30,2024' 
    },
    {
      'author': 'Sahil Kanchankar', 
      'title': 'Blog Post 2',
      'content': 'Second post content',
      'date_posted': 'April 29,2024' 
    },
    {
      'author': 'Arjun Thakur',
      'title': 'Blog Post 3',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Vedant Somalkar',
      'title': 'Blog Post 4',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Prasad Bhalero',
      'title': 'Blog Post 5',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Govinda Patidar',
      'title': 'Blog Post 6',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Akansha Kumari',
      'title': 'Blog Post 7',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Vipin Mahala',
      'title': 'Blog Post 8',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    }
]


# home route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts, title='Home')


# about page route
@app.route("/about")
def about():
    return render_template('about.html',title='About')


# register page route
@app.route("/register", methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!','success')
    return redirect(url_for('home'))
    
  return render_template('register.html', title='Register', form=form)


# login page route
@app.route("/login", methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check username and password','danger')
  return render_template('login.html', title='Login', form=form)




# code runner
if __name__ == '__main__':
    app.run(debug=True)
    
    