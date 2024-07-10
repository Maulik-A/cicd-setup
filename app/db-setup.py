import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' host='localhost'")
except:
    print("I am unable to connect to the database")

# we use a context manager to scope the cursor session
with conn.cursor() as curs:

    try:
        # simple single row system query
        curs.execute("SELECT version()")

        # returns a single row as a tuple
        single_row = curs.fetchone()

        # use an f-string to print the single tuple returned
        print(f"{single_row}")

        # simple multi row system query
        curs.execute("SELECT query, backend_type FROM pg_stat_activity")

        # a default install should include this query and some backend workers
        many_rows = curs.fetchmany(5)

        # use the * unpack operator to print many_rows which is a Python list
        print(*many_rows, sep = "\n")

    # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' host='localhost'")
except:
    print("I am unable to connect to the database")
with conn.cursor() as curs:

    try:
        # simple single row system query
        curs.execute("SELECT * from postgres.public.test")
        single_row = curs.fetchone()
        print(f"{single_row}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
