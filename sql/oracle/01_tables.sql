CREATE TABLE clientes_ref (
  id NUMBER PRIMARY KEY,
  nombre VARCHAR2(120),
  email VARCHAR2(160),
  created_at DATE
);

CREATE TABLE ventas_consolidado (
  id NUMBER PRIMARY KEY,
  cliente_id NUMBER,
  fecha DATE,
  total NUMBER(10,2),
  origen VARCHAR2(30),
  loaded_at DATE
);
