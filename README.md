# ingesta02 — extracción de MySQL a S3

Este contenedor lee todos los registros de una tabla MySQL, crea un CSV con los nombres de las columnas y lo carga a S3. El objeto se guarda en `S3_PREFIX/DB_TABLE/DB_TABLE.csv`.

## Configuración

1. Copia `.env.example` a `.env`.
2. Completa los datos de conexión, el nombre de la tabla y el bucket.
3. No subas `.env` a GitHub. Está excluido en `.gitignore`.
4. La máquina donde se ejecute necesita acceso de red al puerto MySQL y permisos para subir objetos al bucket. Se recomienda usar un rol IAM de la instancia para acceder a S3.

## Construir y ejecutar

```bash
sudo docker build -t ingesta02:guia .
sudo docker run --rm --network host --env-file .env ingesta02:guia
```

Al terminar, el programa muestra la cantidad de registros exportados y la ruta S3 del CSV.
