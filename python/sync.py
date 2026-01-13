import datetime
import mysql.connector
import pymssql
import oracledb
from pathlib import Path

MARIADB = dict(host="127.0.0.1", port=3307, user="dba_mariadb", password="DbaPass!123", database="appdb")
SQLSERVER = dict(server="127.0.0.1", port=11433, user="sa", password="SaPass!12345", database="appdb")
ORACLE_DSN = "127.0.0.1:1522/FREEPDB1"
ORACLE_USER = "dba_oracle"
ORACLE_PASS = "DbaPass!123"

STATE = Path("/tmp/etl_last_sync.txt")

def get_last_sync():
    if STATE.exists():
        return datetime.datetime.fromisoformat(STATE.read_text().strip())
    return datetime.datetime(2000, 1, 1)

def set_last_sync(ts):
    STATE.write_text(ts.isoformat())

def main():
    last = get_last_sync()
    now = datetime.datetime.now()

    # 1) Leer cambios desde MariaDB
    mari = mysql.connector.connect(**MARIADB)
    mc = mari.cursor(dictionary=True)
    mc.execute("""
      SELECT id, cliente_id, fecha, total, created_at, updated_at
      FROM ordenes
      WHERE updated_at > %s
      ORDER BY updated_at ASC
    """, (last,))
    rows = mc.fetchall()
    mc.close()
    mari.close()

    if not rows:
        print(f"[{now}] No hay cambios desde {last}.")
        set_last_sync(now)
        return

    # 2) Upsert a SQL Server
    ms = pymssql.connect(server=SQLSERVER["server"], port=SQLSERVER["port"], user=SQLSERVER["user"], password=SQLSERVER["password"], database=SQLSERVER["database"])
    sc = ms.cursor()
    for r in rows:
        sc.execute("SELECT COUNT(1) FROM ordenes_sync WHERE id=%s", (r["id"],))
        exists = sc.fetchone()[0] == 1
        if exists:
            sc.execute("""
              UPDATE ordenes_sync
              SET cliente_id=%s, fecha=%s, total=%s, created_at=%s, updated_at=%s, synced_at=%s
              WHERE id=%s
            """, (r["cliente_id"], r["fecha"], r["total"], r["created_at"], r["updated_at"], now, r["id"]))
        else:
            sc.execute("""
              INSERT INTO ordenes_sync(id, cliente_id, fecha, total, created_at, updated_at, synced_at)
              VALUES(%s,%s,%s,%s,%s,%s,%s)
            """, (r["id"], r["cliente_id"], r["fecha"], r["total"], r["created_at"], r["updated_at"], now))
    ms.commit()
    sc.close()
    ms.close()

    # 3) Consolidar a Oracle (ventas_consolidado)
    ora = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=ORACLE_DSN)
    oc = ora.cursor()
    for r in rows:
        oc.execute("""
          MERGE INTO ventas_consolidado t
          USING (SELECT :id id FROM dual) s
          ON (t.id = s.id)
          WHEN MATCHED THEN UPDATE SET
            t.cliente_id=:cliente_id,
            t.fecha=:fecha,
            t.total=:total,
            t.origen='MariaDB->SQLServer',
            t.loaded_at=:loaded_at
          WHEN NOT MATCHED THEN INSERT (id, cliente_id, fecha, total, origen, loaded_at)
          VALUES (:id, :cliente_id, :fecha, :total, 'MariaDB->SQLServer', :loaded_at)
        """, dict(
            id=r["id"],
            cliente_id=r["cliente_id"],
            fecha=r["fecha"],
            total=r["total"],
            loaded_at=now
        ))
    ora.commit()
    oc.close()
    ora.close()

    print(f"[{now}] Sync OK: {len(rows)} orden(es) procesadas. last_sync={last} -> {now}")
    set_last_sync(now)

if __name__ == "__main__":
    main()
