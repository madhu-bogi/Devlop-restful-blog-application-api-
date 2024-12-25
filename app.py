from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Blog Post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def _repr_(self):
        return f'<BlogPost {self.title}>'

# Create the database
with app.app_context():
    db.create_all()

# Endpoint to get all blog posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = BlogPost.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])

# Endpoint to get a single blog post by ID
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = BlogPost.query.get_or_404(id)
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content})

# Endpoint to create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully!'}), 201

# Endpoint to update an existing blog post by ID
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = BlogPost.query.get_or_404(id)
    data = request.get_json()

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    db.session.commit()
    return jsonify({'message': 'Post updated successfully!'})

# Endpoint to delete a blog post by ID
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)