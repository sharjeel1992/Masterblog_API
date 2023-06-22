POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

post_id = 2
title = "this is updated post"
content = "another update"
post = next((post for post in POSTS if post["id"] == post_id), None)
if not post:
    print({"error": f"Post with ID {id} not found"})

new_dict = {"id": post_id, "title": post["title"], "content": post["content"]}
post.update(new_dict)

print(POSTS)