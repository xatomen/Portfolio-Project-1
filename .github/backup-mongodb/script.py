# Generar backup de una base de datos MongoDB a través de pymongo

import os
import pymongo
import datetime
# Importamos dotenv para cargar las variables de entorno desde el archivo .env en un ambiente de desarrollo
from dotenv import load_dotenv
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a MongoDB
print("Cargando variables de entorno...")
MONGO_URI = os.getenv("MONGO_URI") # URI de conexión a MongoDB
DB_NAME = os.getenv("DB_NAME") # Nombre de la base de datos a respaldar
BACKUP_DIR = os.getenv("BACKUP_DIR", "/tmp/mongo_backup") # Directorio donde se guardará el backup
BACKUP_FILENAME = f"{DB_NAME}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
BACKUP_FILE = os.path.join(BACKUP_DIR, BACKUP_FILENAME) # Nombre del archivo de backup

# Crear el directorio de backup si no existe
print(f"Creando directorio de backup en: {BACKUP_DIR}")
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Conectar a MongoDB
print(f"Conectando a MongoDB en: {MONGO_URI}")
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# Verificar la conexión a la base de datos
print(f"Conectado a la base de datos: {DB_NAME}")
if db.name != DB_NAME:
    print(f"Error: No se pudo conectar a la base de datos '{DB_NAME}'")
    exit(1)

# Obtener todas las colecciones de la base de datos
print(f"Obteniendo colecciones de la base de datos: {DB_NAME}")
collections = db.list_collection_names() # Lista de colecciones en la base de datos

# Crear un archivo JSON para almacenar el backup
print(f"Creando archivo de backup: {BACKUP_FILE}")
with open(BACKUP_FILE, 'w') as backup_file:
    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find()
        
        # Escribir los documentos de la colección en el archivo JSON
        for document in documents:
            backup_file.write(f"{document}\n")

# Comprimimos el archivo de backup en formato tarball
import tarfile
print(f"Comprimendo el archivo de backup: {BACKUP_FILE}.tar.gz")
with tarfile.open(f"{BACKUP_FILE}.tar.gz", "w:gz") as tar:
    tar.add(BACKUP_FILE, arcname=os.path.basename(BACKUP_FILE))

# Exportamos la ruta del archivo comprimido como output del action
print(f"Exportando la ruta del archivo comprimido: {BACKUP_FILENAME}.tar.gz")
os.environ["BACKUP_FILENAME"] = f"{BACKUP_FILENAME}.tar.gz"

# Cerrar la conexión a MongoDB
print("Cerrando conexión a MongoDB...")
client.close()
print(f"Backup de la base de datos '{DB_NAME}' completado. Archivo guardado en: {BACKUP_FILE}")