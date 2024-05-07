import os
import secrets
from PIL import Image
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required 


# home route 
@app.route("/")
@app.route("/home")
def home():
  posts = Post.query.all()
  return render_template('home.html',posts=posts, title='Home')
  
# about page route
@app.route("/about")
def about():
    return render_template('about.html',title='About')


# register page route
@app.route("/register", methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
    
  form = RegistrationForm()
  if form.validate_on_submit():
    hash_pass = bcrypt.generate_password_hash(form.password.data)
    user = User(username=form.username.data,email=form.email.data, password=hash_pass)
    db.session.add(user)
    db.session.commit()
    
    flash(f'Account created for {form.username.data}!','success')
    return redirect(url_for('login'))
    
  return render_template('register.html', title='Register', form=form)


# login page route
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
    
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      # if any query parameter
      next_page = request.args.get('next')
       
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check email and password','danger')
  return render_template('login.html', title='Login', form=form)


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _,f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
  
  output_size = (125,125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  return picture_fn

# logout route
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))

# account route
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
  form = UpdateAccountForm()
  
  if form.validate_on_submit():
    
    if form.picture.data:
      picture = save_picture(form.picture.data)
      current_user.image_file = picture   

    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('your account has been updated!','success')
    return redirect(url_for('account')) # post get redirect pattern
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    
  image_file = url_for('static',filename='profile_pics/'+ current_user.image_file)
  return render_template('account.html', title='Account',image_file=image_file, form=form)


# add posts 
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created!', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', form=form, legend='New Post') 


# specified Id post
@app.route('/post/<int:post_id>')
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html',title=post.content, post=post)


# update post
@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
    
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash('Your post has been updated!','success')
    return redirect(url_for('post',post_id= post.id))
  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content
    
  return render_template('create_post.html', title='Update Post', form=form, legend='Update Post') 

# update post
@app.route('/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
    
  db.session.delete(post)
  db.session.commit()
  
  flash('Your post has been deleted','success')
  return redirect(url_for('home'))
  
