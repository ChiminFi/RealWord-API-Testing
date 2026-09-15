from src.db.db_client import execute_query


def test_select_one():
    assert execute_query("SELECT 1;") == [(1,)]


def test_query_realworld_table_names():
    rows = execute_query(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    )
    table_names = {row[0] for row in rows}

    assert {
        "accounts_user",
        "articles_article",
        "comments_comment",
    } <= table_names
