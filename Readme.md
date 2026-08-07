# 🎬 Módulo Odoo 15 - Gestión de Videoclub

Este repositorio contiene un módulo personalizado desarrollado para **Odoo 15** que permite la gestión integral de un videoclub. El proyecto abarca desde el modelado de datos (MER) hasta la implementación de la lógica de negocio y la seguridad en el framework de Odoo.

## 🚀 Características Principales

El sistema está diseñado para gestionar el catálogo y el flujo de alquileres mediante los siguientes módulos lógicos:
*   **Catálogo:** Gestión de películas (`videoclub.movie`), géneros (`videoclub.genre`) y directores (`videoclub.director`).
*   **Inventario:** Control del estado físico de las copias o cintas individuales (`videoclub.tape`).
*   **Alquileres:** Registro del flujo de préstamos y devoluciones (`videoclub.rental`).
*   **Seguridad (RBAC):** Roles definidos mediante Listas de Control de Acceso (ACLs) y Reglas de Registro (`ir.rule`):
    *   **Cliente:** Puede navegar por el catálogo y gestionar exclusivamente sus propios alquileres.
    *   **Manager:** Tiene acceso total (CRUD) para la administración del videoclub.

---

## 🛠️ Requisitos Previos

Para desplegar este módulo en tu entorno local, asegúrate de contar con las siguientes herramientas:

*   **Odoo:** Versión 15.0
*   **Python:** Versión 3.9.25
*   **Base de Datos:** PostgreSQL (configurado y enlazado con Odoo)

---

## ⚙️ Instalación y Ejecución

Clona este repositorio dentro de la carpeta de `custom_addons` de tu instalación de Odoo. Asegúrate de tener activo tu entorno virtual (`venv`).

### 1. Primera Ejecución (Instalación limpia)
Para arrancar el servidor, crear la base de datos e instalar el módulo por primera vez, ejecuta el siguiente comando en tu terminal:

```bash
python3 odoo-bin -c odoo.conf -d videoclub_db -i videoclub
