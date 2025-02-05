# Proyecto Urban Routes 

Alumno: Cristopher Antonio Garza Bustamante
Cohort: 22

## _Proyecto para TripleTen QA Sprint 8_

En este proyecto haremos pruebas automatizadas para la aplicación de prueba "Urban Routes", específicamente un uso completo de la funcionalidad de pedir un viaje en taxi con parametros establecidos

Se utilizó lo aprendido en el modulo actual con algo de conocimiento de lo visto en el curso de Data Scientist y leyendo la documentación de https://cnt-00325675-2c3c-4aef-b3b7-805610c2765a.containerhub.tripleten-services.com/docs para realizar las pruebas.

Se utilizó el siguiente IDE para realizar el proyecto y correr las pruebas:
- PyCharm 2024.3.2 (Community Edition)
- Build #PC-243.23654.177, built on January 27, 2025
- Runtime version: 21.0.5+8-b631.30 amd64 (JCEF 122.1.9)
- VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
- Toolkit: sun.awt.windows.WToolkit
- Windows 10.0
- GC: G1 Young Generation, G1 Concurrent GC, G1 Old Generation
- Memory: 4090M
- Cores: 8
- Registry:
 - ide.experimental.ui=true
 - llm.show.ai.promotion.window.on.start=false
- Non-Bundled Plugins:
 - com.intellij.plugins.vscodekeymap (243.21565.122)


Instrucciones para ejecutar las pruebas
- Tener instalado Python. Al tiempo de creación del proyecto se utilizó la versión 3.12
- Un entorno base funcional, de preferencia es mejor tener uno exclusivo para el proyecto con conda. Para más información revise la siguiente dirección: https://www.campusmvp.es/recursos/post/como-gestionar-diferentes-entornos-para-python-con-conda.aspx  
- Instalar las dependencias, para mayor orden se localizan en el archivo requirements.txt. Utilizar el siguiente comando desde la raíz del proyecto: *pip install -r requirements*
- Instalar pytest: *pip install pytest*
- En el archivo *configuration.py* cambiar la variable URL_SERVICE por la URL del servidor actual y activo de Urban Routes
- Ejecutar desde consola, donde "root" es la carpeta base donde se encuentra el proyecto: *pytest root/main.py*

Estructura del proyecto:
- root
  - .gitignore: archivos a ignorar en repositorio git
  - data.py: variables para pruebas en Urban Routes
  - main.py: archivo principal de las pruebas  
  - README.md: este archivo
  - requirements.txt: archivo con las dependencias del proyecto
  