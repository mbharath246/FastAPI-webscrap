import psycopg2

class WebScrap:
    # database connection
    def db_connection():
        conn = psycopg2.connect(
            host="172.17.0.1",
            port="5433",
            dbname="scrap",
            user="postgres",
            password="bharath",
        )
        cur = conn.cursor()
        return conn, cur


    # titles
    def scrap_title(soup):
        titles = soup.find_all("h2", class_="home-title")
        titles_list = [title.text for title in titles]
        return titles_list


    # images
    def scrap_images(soup):
        images = soup.find_all("img", class_="home-img-src lazyload")
        images_list = [image["data-src"] for image in images]
        return images_list


    # urls
    def scrap_urls(soup):
        urls = soup.find_all("a", class_="story-link")
        urls_list = [url["href"] for url in urls]
        return urls_list


    # description
    def scrap_description(soup):
        descriptions = soup.find_all("div", class_="home-desc")
        descriptions_list = [desc.text for desc in descriptions]
        return descriptions_list


    # scraping from web pages
    def scrap_webpage(titles_list, urls_list, images_list, descriptions_list):
        try:
            conn, cur = WebScrap.db_connection()

            cur.execute("DROP TABLE IF EXISTS blog_description CASCADE;")
            cur.execute("DROP TABLE IF EXISTS generalise_description CASCADE;")
            cur.execute("DROP TABLE IF EXISTS blogs CASCADE;")

            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS blogs(
                id SERIAL PRIMARY KEY,
                url TEXT,
                heading TEXT
            );
            """
            )
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS blog_description(
                id SERIAL PRIMARY KEY,
                url TEXT ,
                description TEXT,
                image TEXT,
                FOREIGN KEY (id) REFERENCES blogs(id)
            );
            """
            )
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS generalise_description(
                id SERIAL PRIMARY KEY,
                description TEXT,
                FOREIGN KEY (id) REFERENCES blogs(id)
            );
            """                
            )
            for title, url, image, desc in zip(
                titles_list, urls_list, images_list, descriptions_list
            ):
                blog_rows = [url, title]
                meta_data_rows = [url, image, desc]
                cur.execute(
                    "INSERT INTO blogs (url,heading) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                    blog_rows,
                )

                cur.execute(
                    "INSERT INTO blog_description (url, image, description) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    meta_data_rows,
                )

        except (Exception) as e:
            print("Error :", e)

        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()


    # to show blog data
    def show_data_blogs(column):
        try:
            conn, cur = WebScrap.db_connection()
            cur.execute(f"SELECT {column} FROM blogs;")
            records = cur.fetchall()
            for record in records:
                yield record

        except (psycopg2.errors.UndefinedTable,Exception) as e:
            return {'Error' : e}
        
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()


    # show blog_description details 
    def show_blog_description(column):
        try:
            conn, cur = WebScrap.db_connection()
            cur.execute(f"SELECT {column} FROM blog_description;")
            records = cur.fetchall()
            for record in records:
                yield record

        except (psycopg2.errors.UndefinedTable,Exception) as e:
            return {'Error' : e}
        
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()

    # show generalised_description details
    def get_generalise_blog(column):
        try:
            conn, cur = WebScrap.db_connection()
            cur.execute(f"SELECT {column} FROM generalise_description;")
            for record in cur.fetchall():
                yield record

        except (Exception, psycopg2.errors.UndefinedTable) as e:
            return {"Error ": e}
        
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()


    # show stop-words details
    def get_stop_words_count():
        try:
            conn, cur = WebScrap.db_connection()
            cur.execute("SELECT stop_words FROM count_stop_words;")
            for record in cur.fetchall():
                yield record

        except (Exception, psycopg2.errors.UndefinedTable) as e:
            return {"Error ": e}
        
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()