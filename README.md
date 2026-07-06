# Entregable 5 - Agente IA RAG con Azure SQL, ACR, ACA y Azure DevOps

Solucion docente para construir una API FastAPI con arquitectura RAG, contenerizarla con Docker, probarla con Docker Compose, publicar la imagen en Azure Container Registry y desplegarla en Azure Container Apps mediante Azure DevOps Pipelines.

## 1. Estructura

```text
api.py                 Endpoints FastAPI: /, /health, /knowledge, /ask, /ingest
agent.py               Logica RAG: embedding de pregunta, retrieval y respuesta
ai_provider.py         Modo demo o modo OpenAI
settings.py            Configuracion por variables de entorno
db.py                  Conexion a Azure SQL y creacion de tabla
init_db.py             Carga inicial de conocimiento
Dockerfile             Imagen Docker de la API
docker-compose.yml     Ejecucion local del contenedor
azure-pipelines.yml    CI/CD Azure DevOps
```

## 2. Ejecucion local

```bash
copy .env.example .env
# editar .env con la cadena de conexion real de Azure SQL

docker compose build
docker compose run --rm agent python init_db.py
docker compose up -d
```

Abrir:

- http://localhost:8000
- http://localhost:8000/health
- http://localhost:8000/docs

## 3. Prueba del agente

```powershell
$body = @{ question = "Que papel cumple Azure Container Apps en esta practica?" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/ask" -ContentType "application/json" -Body $body
```

## 4. Azure DevOps

Crear dos service connections:

- `sc-azure-entregable5`: Azure Resource Manager contra la suscripcion.
- `sc-acr-entregable5`: Docker Registry contra Azure Container Registry.

Crear variables secretas en el pipeline o en un Variable Group:

- `AZURE_SQL_CONNECTION_STRING`
- `OPENAI_API_KEY` (puede ir vacia si usas `LLM_PROVIDER=demo`)
- `ACR_USERNAME`
- `ACR_PASSWORD`

Ajustar en `azure-pipelines.yml` los nombres reales de ACR, grupo de recursos, Container App y entorno ACA.
