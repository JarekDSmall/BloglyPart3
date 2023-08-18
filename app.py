from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'your-secret-key'  # Set your secret key for flash messages

# Initialize SQLAlchemy and Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Routes

@app.route('/')
def index():
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        bio = request.form['bio']
        profile_picture = request.form['profile_picture']

        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, bio=bio, profile_picture=profile_picture)

        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!')
        return redirect(url_for('show_users'))

    return render_template('new.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.profile_picture = request.form['profile_picture']
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))

# Routes for posts
@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title, content=content, user_id=user.id) 
        db.session.add(new_post)
        db.session.commit()

        flash('Post added successfully!')
        return redirect(url_for('user_detail', user_id=user_id))

    return render_template('add_post.html', user=user)

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post_id))

    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id  # Save the user_id before deleting the post
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('user_detail', user_id=user_id))

# Routes for tags
@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        name = request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash('Tag added successfully!')
        return redirect(url_for('show_tags'))
    return render_template('tags/new.html')

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        flash('Tag updated successfully!')
        return redirect(url_for('show_tags'))
    
    return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully!')
    return redirect(url_for('show_tags'))


if __name__ == '__main__':
    app.run(debug=True)


