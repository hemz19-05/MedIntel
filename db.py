import os
from sqlalchemy import create_engine, text

def get_engine():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError('DATABASE_URL is missing. Add it in Render Environments Variables.')
    
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)


    return create_engine(database_url, pool_pre_ping=True)

def init_db():
    engine = get_engine()

    create_query_logs_table = """
    CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    drug_name TEXT NOT NULL,
    variant TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_query_logs_table))
        conn.commit()

