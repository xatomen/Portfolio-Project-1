# Proyecto: Gestión de Base de Datos MongoDB Atlas como IaC y Backup en S3 Bucket

## Descripción
Este proyecto tiene como objetivo crear un pipeline que permite gestionar una base de datos en MongoDB Atlas como Infraestructura como Código (IaC) utilizando Terraform. Además, incluye la capacidad de realizar backups de la base de datos y almacenarlos en un bucket S3 de AWS.

## Tecnologías Utilizadas
- **Terraform**: Para aprovisionar y gestionar la base de datos.
- **GitHub Actions**: Para la automatización de workflows y composite actions.
- **Python**: Para la creación de scripts que generan los backups.
- **AWS S3**: Para almacenar tanto el estado de Terraform (tfstate) como los backups de la base de datos.
- **MongoDB Atlas**: La base de datos se encuentra en una instancia M0 free tier sin backup automático.

## Funcionalidades Principales
1. **Aprovisionamiento de la Base de Datos**:
   - Utiliza Terraform para aprovisionar una base de datos M0 Azure en MongoDB Atlas.
   - El estado de Terraform (tfstate) se gestiona a través de un backend almacenado en un bucket S3 de AWS.

2. **Creación y Almacenamiento de Backups**:
   - Un script en Python genera backups de la base de datos.
   - Los backups se comprimen y se suben automáticamente al bucket S3 de AWS mediante GitHub Actions.

## Workflows
El proyecto incluye dos workflows principales:

1. **Provisionar la Base de Datos**:
   - Aprovisiona la base de datos en MongoDB Atlas utilizando Terraform.

2. **Backup de la Base de Datos**:
   - Genera un backup de la base de datos.
   - Sube el backup generado al bucket S3 de AWS.

## Estructura del Proyecto
```
Portfolio-Project-1/
├── LICENSE
├── README.md
├── .github/
│   ├── workflows/
│   │   ├── provision-db.yml
│   │   └── backup-db.yml
│   ├── actions/
│   │   ├── backup-action/
│   │   │   ├── action.yml
│   │   │   ├── backup.py
│   │   │   └── requirements.txt
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── terraform.tfstate
│   ├── terraform.tfstate.backup
│   └── terraform.tfvars
```

## Requisitos Previos
- Tener configuradas las credenciales de AWS para acceder al bucket S3.
- Tener una cuenta en MongoDB Atlas.
- Instalar las siguientes herramientas:
  - Terraform
  - Python
  - Docker (opcional, para pruebas locales)

## Uso
1. **Provisionar la Base de Datos**:
   - Ejecutar el workflow correspondiente en GitHub Actions.

2. **Realizar un Backup**:
   - Ejecutar el workflow de backup en GitHub Actions.

## Licencia
Este proyecto está licenciado bajo los términos especificados en el archivo `LICENSE`.