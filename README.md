# ChinaWok Analítica - Sistema de Consultas AWS Athena

Sistema automatizado de lambdas para ejecutar consultas analíticas sobre datos de ChinaWok almacenados en AWS Athena.

## Configuración Requerida

### 1. Credenciales AWS (~/.aws/credentials)

Las credenciales deben estar configuradas en tu máquina local:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
aws_session_token = YOUR_SESSION_TOKEN  # Opcional
```

### 2. Región AWS (~/.aws/config)

La región se configura en el archivo config:

```ini
[default]
region = us-east-1
```

Si no existe este archivo, el sistema usará **us-east-1** por defecto.

### 3. Variables de Entorno (.env)

Copia `.env.example` a `.env` y configura:

- **AWS_ACCOUNT_ID**: Tu Account ID de AWS
- **SERVERLESS_ORG**: Tu organización en Serverless Framework
- **ATHENA_DATABASE**: Nombre de la base de datos en Glue/Athena
- **ATHENA_OUTPUT_LOCATION**: Bucket S3 para resultados de queries
- **ATHENA_WORKGROUP**: Workgroup de Athena (primary por defecto)
- **DEFAULT_LOCAL_ID**: Local ID por defecto para testing

## Lambdas Disponibles

### 1. Productos Más Vendidos
**Endpoint**: `POST /analitica/productos-vendidos`

```json
{
  "local_id": "LOCAL-0001"
}
```

### 2. Mejor Personal
**Endpoint**: `POST /analitica/mejor-personal`

```json
{
  "local_id": "LOCAL-0001"
}
```

### 3. Récord Diario
**Endpoint**: `POST /analitica/record-diario`

```json
{
  "local_id": "LOCAL-0001",
  "year": 2025,
  "month": 1
}
```

### 4. Estadísticas Generales
**Endpoint**: `POST /analitica/estadisticas-generales`

```json
{
  "local_id": "LOCAL-0001"
}
```

## Despliegue

```bash
# Instalar dependencias
npm install

# Desplegar a AWS
serverless deploy

# Desplegar función específica
serverless deploy function -f productosVendidos
```

## Permisos IAM (LabRole)

El LabRole debe tener permisos para:
- **Athena**: StartQueryExecution, GetQueryExecution, GetQueryResults
- **Glue**: GetDatabase, GetTable, GetPartitions
- **S3**: GetObject, PutObject en buckets de datos y resultados
