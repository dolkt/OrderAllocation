import os

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("PORT")
    password = os.environ.get("DB_PASSWORD")
    user = os.environ.get("USER")
    db_name = "order_allocation"

    return f"postgresql:psycopg2://{user}:{password}@{host}:{port}/{db_name}"