import psycopg

with psycopg.connect("dbname=KyoDB_ user=postgres password=root") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE Users (
                id serial PRIMARY KEY,
                username text,
                password text,
                iswordscloud boolean DEFAULT FALSE,
                logo integer,
                role text
                )
            """)

        conn.commit()
