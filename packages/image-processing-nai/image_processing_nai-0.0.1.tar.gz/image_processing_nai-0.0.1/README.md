# image-processing

## Descrição

O pacote `image-processing` fornece funcionalidades para processamento básico de imagens, incluindo comparação de
similaridade, redimensionamento de imagens, ajuste de histogramas e plotagem de imagens e histogramas.

## Funcionalidades

### Módulo `processing`

- **`combination.py`**:
    - `find_difference(image1, image2)`: Encontra a diferença estrutural entre duas imagens.
    - `transfer_histogram(image1, image2)`: Transfere o histograma de uma imagem para outra.

- **`transformation.py`**:
    - `resize_image(image, proportion)`: Redimensiona uma imagem para uma determinada proporção.

### Módulo `utils`

- **`io.py`**:
    - `read_image(path, is_gray)`: Lê uma imagem a partir de um caminho.
    - `save_image(image, path)`: Salva uma imagem para um caminho específico.

- **`plot.py`**:
    - `plot_image(image)`: Plota uma única imagem.
    - `plot_result(*args)`: Plota várias imagens lado a lado.
    - `plot_histogram(image)`: Plota o histograma de uma imagem RGB.

## Instalação

1. Clone o repositório para a sua máquina local:
    ```bash
    git clone https://github.com/Nai-nailinha/package-template.git
    ```

2. Navegue para o diretório do pacote:
    ```bash
    cd image-processing
    ```

3. Instale o pacote:
    ```bash
    pip install .
    ```

## Autor

Enaile Lopes
