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

Configura las siguientes variables:

- **AWS_ACCOUNT_ID**: Tu Account ID de AWS
- **ATHENA_DATABASE**: Nombre de la base de datos en Glue/Athena
- **ATHENA_OUTPUT_LOCATION**: Bucket S3 para resultados de queries
- **ATHENA_WORKGROUP**: Workgroup de Athena (primary por defecto)

**Nota**: La variable `SERVERLESS_ORG` está **hardcoded en serverless.yml** porque Serverless Framework no carga el `.env` para el campo `org` en tiempo de login.

## Despliegue

```bash
# 1. Iniciar sesión en Serverless (solo primera vez)
serverless login

# 2. Instalar dependencias
npm install

# 3. Desplegar a AWS
serverless deploy

# 4. Desplegar función específica
serverless deploy function -f productosVendidos
```

## Troubleshooting

### Error: "You are not a member of the Org"
- Verifica que la org en `serverless.yml` coincida con tu cuenta de Serverless
- Ejecuta `serverless login` y confirma tu usuario
- Revisa el archivo `~/.serverlessrc` para ver qué usuario está activo

## Permisos IAM (LabRole)

El LabRole debe tener permisos para:
- **Athena**: StartQueryExecution, GetQueryExecution, GetQueryResults
- **Glue**: GetDatabase, GetTable, GetPartitions
- **S3**: GetObject, PutObject en buckets de datos y resultados

## Ejemplos de Postman

Después del despliegue, obtendrás las URLs de los endpoints. Ejemplo:
```
POST /analitica/productos-vendidos
{
  "local_id": "LOCAL-0001"
}
```
