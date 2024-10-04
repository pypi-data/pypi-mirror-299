
# Kyne Goes Easy Dataflow

`kyne-goes-easy-dataflow` es una colección de funciones genéricas diseñadas para simplificar las operaciones con Google Cloud Platform (GCP). Este paquete facilita la interacción con servicios como Google Cloud Storage, BigQuery, y otros componentes clave de GCP, permitiendo a los desarrolladores integrar estas herramientas de manera más eficiente en sus proyectos.

## Licencia

Este proyecto está licenciado bajo la Kynegos License. Para más detalles, consulta el archivo [LICENSE](./LICENSE).


## Instalación

Para instalar el paquete, utiliza pip:

```bash
pip install kyne-goes-easy-dataflow
```

## Actualización

Para instalar el paquete, utiliza pip:

```bash
pip install --upgrade kyne-goes-easy-dataflow
```

## Uso

### Importar el Paquete

Para comenzar a utilizar las funciones disponibles, simplemente importa el paquete en tu script de Python:

```python
import kynegoes_easy_dataflow.Kynegos_functions as KYNEGOS_FUNCTIONS
```

### Exploración de Funciones

Para ver qué funciones están disponibles en el paquete, puedes utilizar la función `dir()` de Python:

```python
print(dir(KYNEGOS_FUNCTIONS))
```

Esto te mostrará una lista de todas las funciones disponibles en `kyne-goes-easy-dataflow`.

### Ejemplo de Uso

Cada función en el paquete está diseñada para realizar una tarea específica en GCP. Aquí te mostramos un ejemplo básico de cómo utilizar una de las funciones para cargar un archivo a Google Cloud Storage:

```python
# Ejemplo de cómo subir un archivo a Google Cloud Storage
KYNEGOS_FUNCTIONS.upload_to_gcs(bucket_name='nombre_del_bucket', source_file='ruta/del/archivo.txt', destination_blob='carpeta/archivo.txt')
```

### Documentación de Funciones

Para obtener detalles sobre cómo usar cada función, puedes consultar la documentación inline mediante `help()`:

```python
help(KYNEGOS_FUNCTIONS.upload_to_gcs)
```

Esto te proporcionará una descripción detallada de los parámetros y el propósito de la función.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, envíe un correo mediante la plataforma Pypy.org

## Posibles Problemas

### Solución a posibles problemas con `ogr2ogr`

Si al ejecutar el paquete encuentras problemas relacionados con `ogr2ogr`, sigue estos pasos para instalar correctamente GDAL en tu entorno:

#### Paso 1: Actualizar los repositorios e instalar `gdal-bin`

Ejecuta los siguientes comandos en una celda de código o en tu terminal:

```bash
# Actualizar la lista de paquetes
!apt-get update

# Instalar gdal-bin y libgdal-dev
!apt-get install -y gdal-bin libgdal-dev
```

##### Explicación:
- **gdal-bin**: Este paquete incluye las herramientas de línea de comandos de GDAL, como `ogr2ogr`, `gdal_translate`, entre otras.
- **libgdal-dev**: Proporciona los archivos necesarios para desarrollar o compilar extensiones que dependen de GDAL.

#### Paso 2: Verificar que `ogr2ogr` está instalado

Después de la instalación, verifica que `ogr2ogr` está disponible ejecutando el siguiente comando en tu terminal o celda de código en Python:

```bash
!ogr2ogr --version
```

La salida debería ser algo como:

```bash
GDAL 3.4.1, released 2021/12/27
```

#### Paso 3: Verificar en Python que `ogr2ogr` está en el `PATH`

Para asegurarte de que `ogr2ogr` está en el `PATH` y accesible desde Python, ejecuta el siguiente código:

```python
import shutil
print(shutil.which('ogr2ogr'))
```

La salida debería ser algo como:

```bash
/usr/bin/ogr2ogr
```

Esto confirma que `ogr2ogr` está disponible en tu entorno y que Python puede encontrarlo correctamente.

### Crear un directorio si no existe

Si necesitas crear un directorio solo si no existe, puedes usar la siguiente función en tu código:

```python
import os

# Ruta del directorio que deseas crear
directorio = 'ruta/del/directorio'

# Crear el directorio solo si no existe
os.makedirs(directorio, exist_ok=True)
```

Este código creará el directorio especificado, y si ya existe, no lanzará ningún error.
