import csv
import os
import re
import tempfile

import boto3
import mysql.connector


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Falta configurar la variable de entorno {name}.")
    return value


def main():
    db_host = required_env("DB_HOST")
    db_name = required_env("DB_NAME")
    db_user = required_env("DB_USER")
    db_password = required_env("DB_PASSWORD")
    db_table = required_env("DB_TABLE")
    bucket = required_env("S3_BUCKET")

    if not re.fullmatch(r"[A-Za-z0-9_]+", db_table):
        raise ValueError("DB_TABLE solo puede contener letras, números y guion bajo.")

    db_port = int(os.getenv("DB_PORT", "3306"))
    s3_prefix = os.getenv("S3_PREFIX", "raw/ingesta02").strip("/")
    s3_key = f"{s3_prefix}/{db_table}/{db_table}.csv"
    csv_path = None

    connection = mysql.connector.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password,
        connection_timeout=15,
    )

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM `{db_table}`")
        if cursor.description is None:
            raise RuntimeError(f"No se pudo obtener la estructura de la tabla {db_table}.")

        column_names = [column[0] for column in cursor.description]

        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8-sig",
            suffix=".csv",
            delete=False,
        ) as csv_file:
            csv_path = csv_file.name
            writer = csv.writer(csv_file)
            writer.writerow(column_names)

            total_rows = 0
            while True:
                rows = cursor.fetchmany(1000)
                if not rows:
                    break
                writer.writerows(rows)
                total_rows += len(rows)

        boto3.client("s3").upload_file(csv_path, bucket, s3_key)
        print(f"Registros exportados: {total_rows}")
        print(f"CSV cargado en s3://{bucket}/{s3_key}")
        print("Ingesta completada")

    finally:
        connection.close()
        if csv_path and os.path.exists(csv_path):
            os.remove(csv_path)


if __name__ == "__main__":
    main()
