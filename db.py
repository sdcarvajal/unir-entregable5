import pyodbc
from settings import settings


def get_connection():
    """Abre una conexion contra Azure SQL Database usando una variable de entorno."""
    if not settings.azure_sql_connection_string:
        raise RuntimeError(
            "Falta AZURE_SQL_CONNECTION_STRING. Configurala en .env, en Azure DevOps o en los secretos de ACA."
        )
    return pyodbc.connect(settings.azure_sql_connection_string)


def create_table_if_not_exists() -> None:
    """Crea la tabla de conocimiento si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        IF OBJECT_ID('dbo.knowledge_chunks', 'U') IS NULL
        CREATE TABLE dbo.knowledge_chunks (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(255) NOT NULL,
            source NVARCHAR(255) NULL,
            content NVARCHAR(MAX) NOT NULL,
            embedding NVARCHAR(MAX) NOT NULL,
            embedding_model NVARCHAR(100) NOT NULL,
            created_at DATETIME2 DEFAULT SYSUTCDATETIME()
        );
        """
    )
    conn.commit()
    conn.close()
