import psycopg2
import nltk
from nltk.corpus import stopwords
from src.endpoints.webscrap.helper_func import WebScrap


nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words("english"))


def genralise_description():
    try:
        conn, cur = WebScrap.db_connection()
        cur.execute("SELECT description FROM blog_description;")

        records = cur.fetchall()
        for record in records:
            words = nltk.word_tokenize(record[0])
            word_tokens = [word.lower() for word in words if word.isalnum()]
            filtered_words = [word for word in word_tokens if word not in stop_words]
            new_desc = " ".join(filtered_words)

            cur.execute(
                "INSERT INTO generalise_description (description) VALUES (%s) ON CONFLICT DO NOTHING",
                (new_desc,),
            )

    except (psycopg2.errors, Exception) as e:
        return {"Error":e}

    finally:
        if conn:
            conn.commit()
            conn.close()
            cur.close()
