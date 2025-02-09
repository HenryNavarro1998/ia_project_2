# Proyecto de Inteligencia Artificial - Actividad 2

Este proyecto implementa varios algoritmos de inteligencia artificial para resolver problemas específicos. A continuación se describen los archivos principales del proyecto y su funcionalidad.

## Archivos del Proyecto

### `main.py`
Este archivo es el punto de entrada principal del proyecto. Se encarga de coordinar la ejecución de los diferentes algoritmos y gestionar la interacción con el usuario.

### `minimax.py`
Contiene la implementación del algoritmo Minimax, utilizado principalmente en juegos de dos jugadores para tomar decisiones óptimas.

### `q_learning.py`
Implementa el algoritmo de Q-Learning, una técnica de aprendizaje por refuerzo que permite a un agente aprender políticas óptimas a través de la interacción con el entorno.

### `train.py`
Este archivo se encarga de entrenar los modelos de aprendizaje implementados en el proyecto. Incluye funciones para configurar y ejecutar los procesos de entrenamiento.

### `utils.py`
Contiene funciones utilitarias y de apoyo que son utilizadas por los otros módulos del proyecto. Estas funciones pueden incluir manejo de datos, visualización de resultados, entre otros.

### `layout.py`
Define la estructura y el diseño del entorno en el que los algoritmos de inteligencia artificial operan. Este archivo es crucial para la correcta simulación y visualización de los problemas a resolver.

## Instrucciones de Uso

1. Clona el repositorio en tu máquina local.
2. Asegúrate de tener instaladas las dependencias necesarias.
3. Ejecuta `main.py` para iniciar el proyecto y seleccionar el algoritmo que deseas probar.

## Instalación de Dependencias

Para instalar las dependencias necesarias, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

## Ejecución del Entrenamiento del Agente

Para entrenar el agente utilizando los algoritmos implementados, ejecuta el siguiente comando:

```bash
python train.py
```

## Archivo `q_table.json`

Este archivo almacena la tabla Q aprendida por el algoritmo de Q-Learning. La tabla Q contiene los valores de recompensa esperada para cada par estado-acción, lo que permite al agente tomar decisiones informadas basadas en su experiencia previa.

## Requisitos

- Python 3.x
- Librerías adicionales especificadas en `requirements.txt`

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
