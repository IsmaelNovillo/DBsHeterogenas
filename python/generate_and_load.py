from faker import Faker
import random, datetime

import mysql.connector
import pymssql
import oracledb

fake = Faker("es_ES")

MARIADB = dict(host="127.0.0.1", port=3307, user="dba_mariadb", password="DbaPass!123", database="appdb")
SQLSERVER = dict(server="127.0.0.1", port=11433, user="sa", password="SaPass!12345", database="appdb")
ORACLE_DSN = "127.0.0.1:1522/FREEPDB1"
ORACLE_USER = "dba_oracle"
ORACLE_PASS = "DbaPass!123"

def now():
    return datetime.datetime.now()

def main():
    # 1) Generar data base
    clientes = []
    for i in range(1, 101):
        clientes.append((i, fake.name(), fake.email(), now()))

    ordenes = []
    for i in range(1, 301):
        cid = random.randint(1, 100)
        dt = now() - datetime.timedelta(days=random.randint(0, 20))
        total = round(random.uniform(5, 500), 2)
        ordenes.append((i, cid, dt, total, dt, dt))

    # 2) Cargar MariaDB (clientes, ordenes)
    mari = mysql.connector.connect(**MARIADB)
    cur = mari.cursor()
    cur.execute("DELETE FROM ordenes;")
    cur.execute("DELETE FROM clientes;")
    cur.executemany("INSERT INTO clientes(id,nombre,email,created_at) VALUES(%s,%s,%s,%s)", clientes)
    cur.executemany("INSERT INTO ordenes(id,cliente_id,fecha,total,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s)", ordenes)
    mari.commit()
    cur.close()
    mari.close()

    # 3) Cargar Oracle (tabla ref)
    ora = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=ORACLE_DSN)
    oc = ora.cursor()
    oc.execute("DELETE FROM clientes_ref")
    oc.executemany("INSERT INTO clientes_ref(id,nombre,email,created_at) VALUES(:1,:2,:3,:4)", clientes)
    ora.commit()
    oc.close()
    ora.close()

    print("OK: datos generados con Faker y cargados (MariaDB + Oracle).")

if __name__ == "__main__":
    main()
