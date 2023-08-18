from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255)) 

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'

class Post(db.Model):
    """Post model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary=post_tags, backref='posts')

    def __repr__(self):
        return f'<Post id={self.id} title={self.title}>'

class Tag(db.Model):
    """Tag model."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag id={self.id} name={self.name}>'

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)











