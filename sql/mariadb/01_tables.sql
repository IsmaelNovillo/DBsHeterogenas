USE appdb;

CREATE TABLE IF NOT EXISTS clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(120),
  email VARCHAR(160),
  created_at DATETIME
);

CREATE TABLE IF NOT EXISTS ordenes (
  id INT PRIMARY KEY,
  cliente_id INT,
  fecha DATETIME,
  total DECIMAL(10,2),
  created_at DATETIME,
  updated_at DATETIME
);
