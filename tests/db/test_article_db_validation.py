import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


# def test_inspect_article_table():
#     conn = psycopg.connect(
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#     )

#     cursor = conn.cursor()

#     cursor.execute("""
#           SELECT column_name,data_type
#           FROM information_schema.columns
#           WHERE table_name = 'articles_article'
#           ORDER BY ordinal_position
#           """)

#     rows = cursor.fetchall()

#     print(rows)

#     cursor.close()
#     conn.close()


def test_created_article_saved_to_database(
    article_client, logged_in_user, unique_article_data, db_connection
):
    res = article_client.create_article(
        title=unique_article_data["title"],
        description=unique_article_data["description"],
        body=unique_article_data["body"],
        token=logged_in_user["token"],
        tag_list=unique_article_data["tag_list"],
    )

    assert res.status_code == 201
    data = res.json()["article"]

    slug = data["slug"]

    cursor = db_connection.cursor(row_factory=dict_row)
    cursor.execute(
        """
        SELECT slug,title,summary,content
        FROM articles_article
        WHERE slug=%s
            """,
        (slug,),
    )
    row = cursor.fetchone()
    cursor.close()

    assert row is not None
    assert row["slug"] == slug
    assert row["title"] == data["title"]
    assert row["summary"] == data["description"]
    assert row["content"] == data["body"]

    cursor = db_connection.cursor(row_factory=dict_row)
    cursor.execute(
        """
        SELECT *
        FROM accounts_user
        WHERE username=%s
        """,
        (logged_in_user["username"],),
    )
    row_user = cursor.fetchone()

    assert row_user is not None


def test_deleted_article_removed_from_database(
    article_client, article_with_owner, db_connection
):
    slug = article_with_owner["article"]["slug"]
    token = article_with_owner["user"]["token"]

    res = article_client.delete_article(slug=slug, token=token)

    assert res.status_code == 204

    cursor = db_connection.cursor()
    cursor.execute(
        """
        SELECT 1
        FROM articles_article
        WHERE slug=%s
        """,
        (slug,),
    )
    row = cursor.fetchone()
    cursor.close()

    assert row is None


# SELECT table_name
# * FROM information_schema.tables
# WHERE table_schema = 'public'
# ORDER BY table_name;

# SELECT column_name, data_type
# * FROM information_schema.columns
# WHERE table_schema = 'public'
#   AND table_name = 'articles_article'
# ORDER BY ordinal_position;


def test_get_table_user_column(db_connection):
    cursor = db_connection.cursor(row_factory=dict_row)

    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'accounts_user'
        ORDER BY ordinal_position 
        """)
    row = cursor.fetchone()
    print(row)
    # {'column_name': 'id', 'data_type': 'bigint'}
