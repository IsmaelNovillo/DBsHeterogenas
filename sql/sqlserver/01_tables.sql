CREATE DATABASE appdb;
GO

USE appdb;
GO

CREATE LOGIN dba_sqlserver WITH PASSWORD = 'DbaPass!123';
GO
CREATE USER dba_sqlserver FOR LOGIN dba_sqlserver;
GO
ALTER ROLE db_owner ADD MEMBER dba_sqlserver;
GO

CREATE TABLE ordenes_sync (
  id INT PRIMARY KEY,
  cliente_id INT,
  fecha DATETIME2,
  total DECIMAL(10,2),
  created_at DATETIME2,
  updated_at DATETIME2,
  synced_at DATETIME2
);
GO
