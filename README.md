# TFG-Aletheia

# Dependencias del proyecto:
1. docker y docker-compose (sistemas linux y mcos) o docker desktop (sistemas windows)
2. Los datos de conexión para un servidor SMTP (Módulo de suscripcion a notificaciones de cursos creados)
3. Conexión a internet debido a que el proyecto utiliza los gestores de paquetes de docker y python para gestionar las dependencias, una vez generadas las imagenes la primera vez que se levanten los contenedores ya no sería necesaria la conexión, esto se hace para facilitar la instalación.

Utilizando docker-compose el programa automaticamente descarga de los repositorios oficiales de docker y python las librerías necesarias.

Los datos de conexión SMTP deben rellenarse en los campos "smtp_server" y "system_email" del fichero secrets.json que se encuentra en este directorio.


# Contenedores levantados por el docker-compose
1. Servidor Api rest con la app Aletheia a partir del código fuente contenido en este directorio.
2. Servidor de base de datos postgresql (Bajando una imagen del repositorio oficial de docker)
3. Servidor de base de datos mongodb (Bajando una imagen del repositorio oficial de docker)
4. Servidor web de gestion de base de datos postgres (Bajando una imagen del repositorio oficial de docker)
5. Servidor web de gestion de base de datos mongodb (Bajando una imagen del repositorio oficial de docker)

Los puertos donde se levantan los contenedores son configurables a través el fichero docker-compose.yml en este directorio.


# Como desplegar la aplicación y sus dependencias
1. Ejecutar el comando ```docker-compose up -d``` en la raíz de este proyecto para levantar los contenedores.

Esto arrancará la aplicación en el puerto indicado en el docker-compose.yml a la espera de peticiones https que podrían realizarse con postman.

# Como probar los casos de uso implementados en el proyecto
Los test unitarios y de integración con servicios de persistencia y mensajería se encuentran en la carpeta test
Los test de aceptación, usuario o end2end que realizan llamadas a la api rest se encuentran en /apps/acceptance_test

Pueden ejecutarse del siguiente modo:

1. Estando los contenedores levantados ejecutar ```docker exec -it tfg-aletheia-api sh``` para acceder al contenedor con un interprete shell.
2. Ejecutar el comando ```poetry run pytest {{Carpeta raíz de los test}}```.

Ejemplos de ejecución de los test:
1. Ejecutar unit-test y test de integración ```poetry run pytest test```
2. Ejecutar test de aceptación ```poetry run pytest /apps/acceptance_test```
3. Ejecutar todos los test ```poetry run pytest .```