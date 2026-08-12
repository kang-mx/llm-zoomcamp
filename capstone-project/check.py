import dlt

pipeline = dlt.pipeline(
    pipeline_name="handbook_ingestion",
    destination="duckdb",
    dataset_name="handbook_data",
)

with pipeline.sql_client() as client:
    with client.execute_query("""
        SELECT section_title, LEFT(text, 100) AS preview, LENGTH(text) AS len
        FROM handbook_data.handbook_chunks
        LIMIT 10
    """) as cur:
        for row in cur.fetchall():
            print(row)

    with client.execute_query("""
        SELECT COUNT(*) FILTER (WHERE section_title = '') AS no_header_chunks,
               COUNT(*) AS total
        FROM handbook_data.handbook_chunks
    """) as cur:
        print(cur.fetchone())