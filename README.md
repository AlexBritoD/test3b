README.md

Descripción

Esta aplicación es una API RESTful creada en Python utilizando el framework [indicar framework: Django, FastAPI, etc.]. La API permite gestionar productos, inventarios y órdenes, y se asegura de que se dispare una alerta cuando el stock de un producto es inferior a 10 unidades.

Endpoints

La API expone los siguientes endpoints:

POST /api/products: Crea un nuevo producto con sku y name. El nuevo producto se crea con un stock inicial de 100 unidades.
PATCH /api/inventories/product/{PRODUCT_ID}: Agrega stock al producto especificado por PRODUCT_ID.
POST /api/orders: Permite realizar compras de productos.
Características Adicionales

Alertas de Stock Bajo: Un job se ejecuta para disparar una alerta (log en consola) cuando el stock de un producto es inferior a 10 unidades.
Pruebas Unitarias: Se han agregado pruebas unitarias para asegurar la correcta funcionalidad de la API.
Documentación de la API: La documentación de la API está disponible y se puede visualizar utilizando Swagger o Postman.
Requisitos

Python 3.x
Instalación

Clona este repositorio:
sh
Copiar código
git clone [<URL_del_repositorio>](https://github.com/AlexBritoD/test3b.git)
Navega al directorio del proyecto:
sh
Copiar código
cd <nombre_del_directorio>
Instala las dependencias necesarias:
sh
Copiar código
pip install -r requirements.txt
Uso

Inicia la aplicación:
sh
Copiar código
python main.py
La consola generará una URL local.
Para ver los métodos y la documentación, dirígete a la ruta /api/docs.
Docker (Opcional)

Para empaquetar la aplicación en un contenedor Docker, sigue estos pasos:

Construye la imagen de Docker:
sh
Copiar código
docker build -t test3b .
Corre el contenedor:
sh
Copiar código
docker run -p 8000:8000 test3b
Contacto
