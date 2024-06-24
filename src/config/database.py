import os

def get_postgres_uri():
    host = os.environ.get("DB_HOST")
    port = os.environ.get("PORT")
    password = os.environ.get("DB_PASSWORD")
    user = os.environ.get("USER")
    db_name = "product_warehouse"

    return f"postgresql:psycopg2://{user}:{password}@{host}:{port}/{db_name}"