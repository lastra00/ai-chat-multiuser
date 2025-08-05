# Despliegue con Docker

Esta aplicación de chat multi-usuario puede ejecutarse fácilmente usando Docker y Docker Compose.

## Prerrequisitos

- Docker instalado
- Docker Compose instalado
- Clave API de OpenAI

## Configuración Rápida

1. **Clonar/navegar al directorio del proyecto:**
   ```bash
   cd chat_multi_usuario
   ```

2. **Configurar variables de entorno:**
   Crear un archivo `.env` en este directorio:
   ```bash
   echo "OPENAI_API_KEY=tu_clave_api_aqui" > .env
   ```

3. **Ejecutar la aplicación:**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación:**
   Abrir http://localhost:8501 en tu navegador

## Comandos Útiles

### Construcción y ejecución
```bash
# Construir y ejecutar en primer plano
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Detener la aplicación
docker-compose down

# Detener y eliminar volúmenes (reiniciar Redis)
docker-compose down -v
```

### Solo Docker (sin Redis local)

Si ya tienes Redis disponible externamente:

```bash
# Construir la imagen
docker build -t chat-multi-usuario .

# Ejecutar con Redis externo
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=tu_clave_api \
  -e REDIS_URL=redis://tu-redis-host:6379 \
  chat-multi-usuario
```

### Logs y depuración

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de la aplicación
docker-compose logs -f chat-app

# Ver logs solo de Redis
docker-compose logs -f redis

# Acceder al contenedor para depuración
docker-compose exec chat-app bash
```

## Configuración de Producción

Para producción, considera:

1. **Variables de entorno seguras:**
   - Usar secretos de Docker Swarm o Kubernetes
   - No incluir claves API en el código

2. **Persistencia de Redis:**
   - El volumen `redis_data` mantiene los datos entre reinicios
   - Considera backups regulares

3. **Proxy reverso:**
   ```nginx
   # Ejemplo de configuración Nginx
   server {
       listen 80;
       server_name tu-dominio.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Escalabilidad:**
   - Para múltiples instancias, usar Redis externo
   - Considerar load balancer

## Solución de Problemas

### Error de conexión a Redis
```bash
# Verificar que Redis está ejecutándose
docker-compose ps

# Reiniciar Redis
docker-compose restart redis
```

### Error de construcción
```bash
# Limpiar cache de Docker
docker system prune -f

# Reconstruir sin cache
docker-compose build --no-cache
```

### Variables de entorno no cargadas
```bash
# Verificar el archivo .env
cat .env

# Asegurar que está en el directorio correcto
pwd
ls -la .env
``` 