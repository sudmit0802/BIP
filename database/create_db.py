from utils import*

def create_database():
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur_file_path = os.path.dirname(__file__)
    with open(cur_file_path+"/sql/create_db.sql", "r") as f:
        sql = f.read()

    # разбираем SQL-запрос на отдельные запросы
    statements = sqlparse.parse(sql)

    # выполняем каждый запрос по очереди
    for statement in statements:
        query = str(statement).strip()
        if query:
            cur.execute(query)
            
    conn.commit()
    cur.close()
    conn.close()
