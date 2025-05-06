pip install Flask
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []
post_id_counter = 0

def build_tree():
    id_to_post = {post['id']: {**post, 'children': []} for post in posts}
    root_posts = []
    for post in id_to_post.values():
        parent_id = post['parent_id']
        if parent_id is None:
            root_posts.append(post)
        else:
            id_to_post[int(parent_id)]['children'].append(post)
    return root_posts

@app.route('/')
def index():
    post_tree = build_tree()
    return render_template('index.html', posts=post_tree)

@app.route('/post', methods=['POST'])
def post():
    global post_id_counter
    content = request.form['content']
    parent_id = request.form.get('parent_id')
    post_id = post_id_counter
    posts.append({
        'id': post_id,
        'content': content,
        'parent_id': int(parent_id) if parent_id else None
    })
    post_id_counter += 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
