from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_blog_data(data):
    """
    This function will be used with post method to validate the data.
    """
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['POST'])
def get_posts():
    """
    This method handles post-methods requests only on this route.This method will
    fetch data entered by user and will add that to database.This function will
    throw an exception if any of the data is missing.
    """
    if request.method == 'POST':
        data = request.get_json()
        if not validate_blog_data(data):
            return jsonify({"error": "Either title or content data missing"}), 400
        new_id = max(name['id'] for name in POSTS) + 1
        data['id'] = new_id
        title = data['title']
        content = data['content']
        new_post = {"id": new_id, "title": title, "content": content}
        POSTS.append(new_post)
        return jsonify(POSTS), 201


@app.route('/api/posts/<int:id>', methods=["DELETE"])
def delete_blog(id):
    """
    This method will deal with delete request method.First it will match the id with the
    user provided id and delete that post.
    If the user provided id is not found, it will raise
    404 error
    """
    post = next((post for post in POSTS if post["id"] == id), None)
    if not post:
        response = {"error": f"Post with ID {id} not found"}
        return jsonify(response), 404
    POSTS.remove(post)
    return jsonify(f"Post with ID {id} deleted successfully"), 200


@app.route('/api/posts/<int:id>', methods=["PUT"])
def update_blog(id):
    """
    This function will handle update method requests.First it will match the id
    with the id in our database, and if it doesn't exist, it will send an error message.
    If id is found, it will update the id accordingly.
    """
    post = next((post for post in POSTS if post["id"] == id), None)
    if not post:
        response = {"error": f"Post with ID {id} not found"}
        return jsonify(response), 404
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    new_dict = {"id": id, "title": title, "content": content}
    if title is None:
        new_dict = {"id": id, "title": post["title"], "content": content}
    if content is None:
        new_dict = {"id": id, "title": title, "content": post["content"]}
    if title is None and content is None:
        new_dict = post
    post.update(new_dict)
    return jsonify(post), 200


@app.route('/api/posts', methods=["GET"])
def sort_blog():
    """
    This method takes the same route as add post but only deals with get requests.If query string is added
    it will sort the posts based on query string.if no query string is passed it will simply return the posts.
    """
    if request.method == "GET":
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if sort and sort not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field. Allowed values: title, content"}), 400
        if direction and direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort direction. Allowed values: asc, desc"}), 400
        if sort and direction:
            sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=direction == 'desc')
        else:
            sorted_posts = POSTS
        return jsonify(sorted_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
