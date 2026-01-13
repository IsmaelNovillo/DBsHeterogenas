# 🚀 **Instrucciones de Instalación - Plataforma de Base de Datos Heterogénea Interconectada**

## **Requisitos Previos**

Antes de comenzar con la instalación, asegúrate de tener los siguientes requisitos:

- **Sistema Operativo:** Ubuntu 20.04 o superior, o cualquier distribución Linux compatible.
- **Docker y Docker Compose:** necesarios para levantar los contenedores de bases de datos.
- **Python 3.8 o superior** y **pip** instalados.

---

## 1. **Clonar el Repositorio**

Comienza por clonar el repositorio desde GitHub:

```bash
git clone https://github.com/IsmaelNovillo/DBsHeterogenas.git
cd DBsHeterogenas

### A. **Instalar Docker**

Si Docker no está instalado, ejecuta lo siguiente:

```bash
sudo apt update
sudo apt install -y docker.io

Verifica la instalación:

docker --version

B. Instalar Docker Compose

Para instalar Docker Compose v2 (recomendado):

sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose


Hazlo ejecutable:

sudo chmod +x /usr/local/bin/docker-compose


Verifica la instalación:

docker-compose --version

3. Crear la Máquina Virtual (VM)

Si no tienes una VM, sigue estos pasos para crearla con Ubuntu:

RAM recomendada: 8 GB mínimo

CPU recomendada: 2 núcleos mínimo

Disco recomendado: 50 GB mínimo

Si usas VirtualBox, asegúrate de usar Red Bridged para acceder desde tu red local.

4. Configurar Docker y los Contenedores

Dentro de la carpeta clonada DBsHeterogenas, tienes el archivo docker-compose.yml. Este archivo se encargará de levantar los contenedores para MariaDB, SQL Server y Oracle DB.

A. Editar puertos (opcional)

Si necesitas cambiar los puertos predeterminados para MariaDB, SQL Server o Oracle, edita el archivo docker-compose.yml y ajusta las líneas de puertos.

B. Levantar los contenedores

Ejecuta los siguientes comandos en la raíz del repositorio:

docker-compose up -d


Esto levantará los tres contenedores (MariaDB, SQL Server y Oracle). Si todo está bien, puedes verificar los contenedores corriendo con:

docker ps

5. Instalar y Configurar el Entorno Python
A. Crear un entorno virtual

Dentro de la carpeta /python, crea y activa un entorno virtual con:

cd python
python3 -m venv .venv
source .venv/bin/activate

B. Instalar dependencias

Una vez que el entorno virtual esté activo, instala las dependencias necesarias para el proyecto:

pip install --upgrade pip
pip install faker mysql-connector-python pymssql oracledb

6. Configurar el Cron (Tarea programada)

Para que el proceso ETL (sincronización de datos entre los motores de bases de datos) se ejecute automáticamente cada minuto, configura cron.

Abre el archivo de cron con:

crontab -e


Agrega la siguiente línea para ejecutar el script sync.py cada minuto:

*/1 * * * * /home/usuario/db/heterodb/python/.venv/bin/python /home/usuario/db/heterodb/python/sync.py >> /home/usuario/db/heterodb/evidence/logs/etl.log 2>&1


Asegúrate de reemplazar usuario con tu nombre de usuario real.

7. Conectar desde DBeaver

Para conectar los tres motores de bases de datos desde DBeaver, sigue estos pasos:

MariaDB:

Host: IP_DE_LA_VM

Puerto: 3307

Usuario: dba_mariadb

Contraseña: DbaPass!123

Base de datos: appdb

SQL Server:

Host: IP_DE_LA_VM

Puerto: 11433

Usuario: sa

Contraseña: SaPass!12345

Base de datos: appdb

Oracle:

Host: IP_DE_LA_VM

Puerto: 1522

Service Name: FREEPDB1

Usuario: dba_oracle

Contraseña: DbaPass!123

8. Verificación y Logs

Verifica que todo esté funcionando correctamente:

Ver los logs del cron:

tail -f /home/usuario/db/heterodb/evidence/logs/etl.log


Ver el conteo de registros en cada base de datos:

MariaDB:

SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM ordenes;


SQL Server:

SELECT COUNT(*) FROM ordenes_sync;


Oracle:

SELECT COUNT(*) FROM clientes_ref;
SELECT COUNT(*) FROM ventas_consolidado;

9. Acceder al Repositorio en GitHub

El repositorio con todo el código y documentación está disponible en el siguiente enlace:

Repositorio GitHub

Notas Importantes

Oracle Database Free puede tardar más tiempo en levantar. Ten paciencia si ves que tarda más de 5 minutos.

El script ETL (sync.py) se ejecuta cada minuto de forma automática, pero puede ser ejecutado manualmente desde el entorno Python con:

python sync.py
