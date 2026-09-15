import uuid


def make_user_data() -> dict:
    suffix = uuid.uuid4().hex[:8]

    return {
        "username": f"qa_{suffix}",
        "email": f"qa_{suffix}@example.com",
        "password": "TestPassword123!",
    }


def make_article_data() -> dict:
    suffix = uuid.uuid4().hex[:8]

    return {
        "title": f"Test Article {suffix}",
        "description": "Test article description",
        "body": "This is a test article body",
        "tag_list": ["test", "api"],
    }


def make_comment_data() -> dict:
    suffix = uuid.uuid4().hex[:8]

    return {"comment": {"body": f"qa_comment_{suffix}"}}


# print(make_user_data())
# print(make_user_data())
