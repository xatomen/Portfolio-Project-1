# Provisionaremos una base de datos MongoDB en MongoDB Atlas con el tier free

# Añadimos las variables necesarias para el archivo main.tf
variable "public_key" {
  description = "La clave pública para autenticar con MongoDB Atlas"
  type        = string
}

variable "private_key" {
  description = "La clave privada para autenticar con MongoDB Atlas"
  type        = string
}

variable "project_name" {
  description = "El nombre del proyecto en MongoDB Atlas"
  type        = string
}

variable "org_id" {
  description = "El ID de la organización en MongoDB Atlas"
  type        = string
}

variable "cluster_name" {
  description = "El nombre del cluster en MongoDB Atlas"
  type        = string
}

variable "public_ip" {
  description = "La IP pública desde la que se accederá a la base de datos"
  type        = string
}

variable "password" {
  description = "La contraseña del usuario de la base de datos"
  type        = string
}

variable "username" {
  description = "El nombre de usuario para la base de datos"
  type        = string
}

# Configuramos el provider de MongoDB Atlas
provider "mongodbatlas" {
  public_key  = var.public_key
  private_key = var.private_key
  is_mongodbgov_cloud = false
}

# Creamos un proyecto en MongoDB Atlas
resource "mongodbatlas_project" "project" {
  name   = var.project_name
  org_id = var.org_id
}

# Creamos un cluster en MongoDB Atlas
resource "mongodbatlas_cluster" "cluster" {
  project_id = mongodbatlas_project.project.id
  name       = var.cluster_name
  provider_name = "TENANT"
  backing_provider_name = "AWS"
  provider_region_name = "US_EAST_1"
  provider_instance_size_name = "M0" # Free tier
  # mongo_db_major_version = "4.4"
  # backup_enabled = false # No habilitamos el backup para el tier free
}

# Configurar el acceso a la base de datos
resource "mongodbatlas_database_user" "db_user" {
  username   = var.username
  password   = var.password
  project_id = mongodbatlas_project.project.id
  auth_database_name = "admin"
  roles {
    role_name     = "readWrite"
    database_name = "admin"
  }
}

# Configurar la IP de acceso a la base de datos
resource "mongodbatlas_project_ip_access_list" "ip_access_list" {
  project_id = mongodbatlas_project.project.id
  cidr_block = var.public_ip
}