import psycopg2
from src.endpoints.webscrap.helper_func import WebScrap

def create_count_stop_words():
    try:
        conn, cur = WebScrap.db_connection()
        cur.execute("DROP TABLE IF EXISTS count_stop_words;")

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS count_stop_words(
                id SERIAL PRIMARY KEY,
                stop_words TEXT
            );
            """
        )   

        cur.execute('SELECT description FROM generalise_description;')
        records = cur.fetchall()
        records = [rec[0] for rec in records]
        
        for record in records:
            word = {}

            for words in record.split():
                word[words] = record.count(words)
            
            sorted_dict = sorted(word.items(), key=lambda dict_key:dict_key[1], reverse=True)
            word = dict(sorted_dict)
            cur.execute("INSERT INTO count_stop_words (stop_words) VALUES (%s) ON CONFLICT DO NOTHING",(str(word),))

    except (psycopg2.errors, Exception) as e:
        return {"Error":e}

    finally:
        if conn:
            conn.commit()
            conn.close()
            cur.close()