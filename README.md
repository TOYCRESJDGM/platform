# Scrapper & Microservicio de consulta de información de facturas. 

El scrapper tiene como objetivo extraer información de facturas de la DIAN por medio del CUFE, mientras que el microservicio se creo con el objetivo de gestionar la información que se obtiene por medio del scrapper, lo que nos permite consultar esa información. 

## Requisitos del Proyecto

Para implementar esta funcionalidad se utilizo:

1. **Base de Datos**: Una base de datos relacional para almacenar la información de empresas, cargos, personas y calificaciones NPS.

2. **API REST**: Una API RESTful para exponer los endpoints necesarios para la gestión de datos.

3. **Documentación**: Generar una documentación clara y completa de la API para facilitar su uso. 

5. **Despliegue**: Digrama de como desplegar el microservicio en un entorno de producción para su uso continuo. 

## Tecnologías Utilizadas

- **Base de Datos**: MySQL
- **Framework Web**: FastAPI & Flask(Python)
- **Documentación**: Swagger UI
- **Despliegue**: Docker, Google Cloud

## Apectos relevantes
El proyecto en si tiene dos servicios, cada uno con su respectivo dockerfile, por lo cual despues de construir la imagen pueden correr por medio de los contenedores con los comandos:

```bash
docker run -p 6000:6000 scrapper_service
```

```bash
docker run -p 5000:5000 invoice_service
```

O si se prefire tambien se puede usar de manera local, para el caso del microservicio (invoice_service)

```bash
uvicorn main:app --port=5000
```

para el caso del scrapper (scrapper_service), se puede simplemente correr el archivo principal.

```bash
python main.py
```


### Microservicio (Docs)
Toda la documentación relacionada con el microservicio se encuentra en un archivo YAML. Esta documentación puede ser accedida al desplegar la aplicación en la ruta /docs

![image](https://github.com/TOYCRESJDGM/platform/assets/69774985/6369adbd-e2ff-4417-af1b-09ddcbea1787)

![image](https://github.com/TOYCRESJDGM/platform/assets/69774985/dd79df3d-faf7-4811-812e-dd35e9730f14)



### Data Base (Docs)

Se trato de incluir Diagramas que tratasen de explicar la relacion entre las entidades (clases), asi como su diagrama inicial para crear las tablas dentro del archivo init.sql.

![image](https://github.com/TOYCRESJDGM/platform/assets/69774985/5d49fd06-6214-4282-89d9-8e7d0eda33ba)


