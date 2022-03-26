

# Projeto de Estágio


## Descrição:

Criação de um sistema que através do livefeed da camera do ESP32 juntamente com uma rede neural, identifique se o feed contém uma matricula e que o mesmo seja enviado via web para a api da Makewise para que esta retorne os dados contidos na mesma.
Todos os dados de matriculas são registados em bases de dados para serem utilizados no controlo de acessos pelas matriculas com autorização.


### Hardware:
 - Arduino Nano;
 - ESP32CAM.

### Software:
 - Thonny;
 - Google Colab.

### Tech:
- MicroPython; https://github.com/mocleiri/tensorflow-micropython-examples
- Python;
- TensorFlow Lite (tflite);
- Keras;
- Html;
- Git.

	
## Passos:
 1. Criar um programa utilizando a linguagem de programação Python que utilize um conjunto de várias imagens de veículos com matricula e sem matricula e, que o mesmo faça um crop na zona onde está situada a matricula e outro numa zona aleatória com o propósito de criar um dataset para treino.
 1. Criar um modelo de rede neural através do Google Colab e utilizando o Tensorflow Keras que identifique existência matriculas no dataset criado.
 1. Treinar o modelo de rede neural com diversos tipos de camadas de augmentation para melhorar a precisão do mesmo.
 1. Converter a rede neural num modelo TensorFlowlite para este ser utilizado no micro-controlador.
 1. Criar um programa utilizando MicroPython para o ESP32CAM que capture o feed da camera e processe em conjunto com o modelo de rede neural criado, para identificar a existência de matriculas.
 1. Utilizar a api criada pela Makewise para que esta retorne os dados contidos nas matriculas identificadas no feed.
 1. Criar uma base de dados para matriculas identificadas pelo sistema e outra para matriculas autorizadas.
 1. Criar um web server com o ESP32CAM e com páginas criadas com html carregue as bases de dados criadas e possa adicionar e/ou remover autorizações.
 1. Utilizando leds criar um metodo que informe ao utilizador se a matricula identificada tem autorização ou não.
