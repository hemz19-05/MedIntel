from db import get_engine
from sqlalchemy import text


def log_query(drug_name, variant=None):
    """
    Log every drug search into Postgres (continuous analytics)
    """
    engine = get_engine()

    insert_sql = """

    INSERT INTO query_logs (drug_name, variant)
    VALUES (:drug_name, :variant)
    """
    with engine.connect() as conn:
        conn.execute(
            text(insert_sql),
            {'drug_name': drug_name.strip().lower(), 'variant': variant}
        )
        conn.commit()


def get_analytics(limit=20):
    """
    Returns:
    -total_queries
    -unique_drugs
    -drug_list(top searched drugs)
    """
    
    engine = get_engine()

    with engine.connect() as conn:
        total_queries = conn.execute(text('SELECT COUNT(*) FROM query_logs;')).scalar() or 0
        
        unique_drugs = conn.execute(text('SELECT COUNT(DISTINCT drug_name) FROM query_logs;')).scalar() or 0

        top_drugs = conn.execute(
            text("""
                SELECT drug_name, COUNT(*) as counts
                FROM query_logs
                GROUP BY drug_name
                ORDER BY counts DESC
                LIMIT :limit;
            """),
            {'limit': limit}
        ).fetchall()
        
    drug_list = [f'{row[0]} ({row[1]})' for row in top_drugs]

    return {
        'total_queries': total_queries,
        'unique_drugs': unique_drugs,
        'drug_list': drug_list,
    }

