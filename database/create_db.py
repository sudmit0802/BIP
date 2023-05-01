from .utils import*

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

'''
Данный код создает базу данных, используя SQL-запросы, которые хранятся в файле create_db.sql.

Сначала код вызывает функцию get_connection() из модуля utils, которая возвращает объект подключения к базе данных Postgres.

Затем он использует модуль os, чтобы получить путь к директории, в которой находится текущий файл, и открывает файл create_db.sql в этой же директории.

Далее SQL-запросы разбиваются на отдельные запросы с помощью модуля sqlparse, и каждый запрос выполняется отдельно с помощью метода execute() объекта cursor.

После выполнения всех запросов изменения сохраняются с помощью метода commit(), а объекты cursor и connection закрываются с помощью методов close().


'''