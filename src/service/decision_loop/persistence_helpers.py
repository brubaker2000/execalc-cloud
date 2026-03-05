import psycopg2
from src.service.db.postgres import get_conn

def save_decision_entry(tenant_id, user_id, decision_data):
    conn = get_conn()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO decision_journal (tenant_id, user_id, decision_data)
    VALUES (%s, %s, %s) RETURNING id;
    """
    cursor.execute(insert_query, (tenant_id, user_id, decision_data))
    conn.commit()
    entry_id = cursor.fetchone()[0]
    cursor.close()
    return entry_id

def get_decision_entry(entry_id):
    conn = get_conn()
    cursor = conn.cursor()
    select_query = "SELECT * FROM decision_journal WHERE id = %s;"
    cursor.execute(select_query, (entry_id,))
    entry = cursor.fetchone()
    cursor.close()
    return entry

def get_all_decisions_for_tenant(tenant_id):
    conn = get_conn()
    cursor = conn.cursor()
    select_query = "SELECT * FROM decision_journal WHERE tenant_id = %s ORDER BY timestamp DESC;"
    cursor.execute(select_query, (tenant_id,))
    entries = cursor.fetchall()
    cursor.close()
    return entries
