# chatbox-server
Este proyecto permite consultar información sobre enfermedades comunes en perros utilizando un modelo de lenguaje local (Ollama) y un índice de búsqueda rápido basado en embeddings de texto.

## Requisitos

- Python 3.x
- Pip (para instalar las dependencias)

## Instalación

1. Crea un entorno virtual (opcional, pero recomendado):

    ```bash
    python -m venv venv
    ```

2. Activa el entorno virtual:

    - En Windows:
    ```bash
    .\venv\Scripts\activate
    ```

    - En Linux/Mac:
    ```bash
    source venv/bin/activate
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Asegúrate de tener Ollama corriendo en tu máquina local.

5. Coloca tu archivo `context.json` con la información de las enfermedades en el mismo directorio que el script.

## Ejecución de prueba de servidor Ollama

Para ejecutar el archivo de prueba, corre el siguiente comando:

```bash
python3 app/test.py

![diagram](app/assets/modelo_chat_box_diagram.drawio.png)