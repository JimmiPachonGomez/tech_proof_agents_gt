# Prueba técnica de agentes

Este proyecto está contenerizado con Docker para facilitar su configuración y despliegue, además de asegurar la compatibilidad en cualquier dispositivo. Sigue los pasos a continuación para ejecutarlo en tu entorno local:


## 🛠️ Instalación y Requisitos

Asegúrate de tener instalado [Docker](https://www.docker.com/) y **Docker Compose** en tu sistema.

### 1. Clonar el repositorio
Primero, clona este proyecto y accede a la carpeta principal:

```bash
git clone https://github.com/JimmiPachonGomez/tech_proof_agents_gt.git
```
Ubícate en la carpeta donde se encuentra el archivo docket-compose.yml, abre el archivo .env que fué dejado a propósito y coloca una api key de Gemini, guarda y después ejecuta en la terminal:
```bash
docker compose up --build
```

Puede tardar unos minutos en levantar el contenedor ya que también carga una imagen de postgres y una extensión para base de datos vectorial.

Una vez que termina de levantar el contenedor ve a http://localhost:8000/docs, donde podrás ver desplegada localmente la API con la interfaz
que usa FastAPI para documentar, en esa misma sección podrás darle a 'Try it out' para probar cada endpoint.

Las dos peticiones piden únicamente una cadena de texto con la llave 'query'.

En la prueba del agente de reuniones dejé un Guardrail muy exigente, por lo tanto sólo responderá consultas referentes a reuniones. En el caso de pokemón si está muy flexible.
