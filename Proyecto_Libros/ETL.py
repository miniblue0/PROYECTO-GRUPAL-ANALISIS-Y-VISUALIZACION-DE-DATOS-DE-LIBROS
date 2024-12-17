#en este archivo iria el script que llame a todos los anteriores y maneje el flujo de trabajo :3
import os
from extract_data import extract_data, save_raw_data
from transform_data import transform_data
from load_to_datalake import upload_to_s3
from store_data import load_to_sql
from config import S3_BUCKET_NAME, SQL_SERVER_CONNECTION, GOOGLE_BOOKS_API_KEY

def proceso_etl(query, max_results, s3_remote_path):
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__)) #ruta del proyecto
        raw_file_path = os.path.join(project_dir, "raw_books.json") #ruta de los archivos en crudo
        transformed_file_path = os.path.join(project_dir, "transformed_books.json") #ruta de los archivos transformados



        print("Iniciando extracción de datos...")
        books_data = extract_data(query, max_results) #extraigo los datos
        save_raw_data(books_data, raw_file_path)#guardo los datos en crudo
        print("Extracción completada.")

        
        print("Subiendo datos crudos al Data Lake...") 
        upload_to_s3(raw_file_path, S3_BUCKET_NAME, s3_remote_path)#subo los datos crudos al dataLake (amazon S3)
        print("Datos crudos subidos al Data Lake.")        

        
        print("Iniciando transformación de datos...")
        transform_data(raw_file_path, transformed_file_path) #se transforman los datos
        print("Transformación completada.")


        print("Iniciando carga de datos a SQL Server...")
        load_to_sql(transformed_file_path, SQL_SERVER_CONNECTION) #se cargan a sql 
        print("Carga de datos a SQL Server completada.")
        
        ###solo falta el proceso de vista para terminar

    except Exception as e:

        print(f"Error en el proceso ETL: {e}")


if __name__ == "__main__":
    query = "books"
    max_results = 5
    s3_remote_path = "raw_data/raw_books.json" #es la ruta que hay dentro del bucket

    proceso_etl(query, max_results, s3_remote_path)