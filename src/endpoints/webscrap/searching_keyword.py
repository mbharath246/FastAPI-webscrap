import psycopg2
from src.endpoints.webscrap.helper_func import WebScrap


def search_keyword(value:str):
    try:
        conn, cur = WebScrap.db_connection()
        cur.execute("DROP TABLE IF EXISTS blog_keyword;")
        cur.execute(
            """
            CREATE TABLE blog_keyword(
                id SERIAL PRIMARY KEY,
                urls TEXT
            );
            """
        )
        cur.execute(
            f"SELECT b.url FROM generalise_description g,blogs b WHERE b.id = g.id AND g.description LIKE ('%{value}%');"
        )

        records = cur.fetchall()
        for url in records:
            cur.execute("INSERT INTO blog_keyword (urls) VALUES (%s);", (url,))

        cur.execute('SELECT urlS FROM blog_keyword;')
        for url in cur.fetchall():
            yield str(url[0])

    except (Exception, psycopg2.errors.UndefinedTable) as e:
        return {"Error :", e}

    finally:
        if conn:
            conn.commit()
            conn.close()
            cur.close()
