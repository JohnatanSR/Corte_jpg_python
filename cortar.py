import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

# Função para abrir o diálogo e escolher o arquivo ou pasta
def escolher_pasta():
    # Criar a janela principal (não será exibida)
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    # Abrir o diálogo para escolher a pasta
    caminho_pasta = filedialog.askdirectory(title="Escolha a pasta com imagens JPG")
    return caminho_pasta

def crop_whitespace(image_path, output_path):
    # Verifica se o arquivo existe
    if not os.path.isfile(image_path):
        print(f"Erro: O arquivo {image_path} não foi encontrado.")
        return

    # Carrega a imagem
    image = cv2.imread(image_path)

    if image is None:
        print(f"Erro: Não foi possível carregar a imagem {image_path}.")
        return

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica um limiar para destacar os elementos não-brancos
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Encontra os contornos dos elementos não-brancos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Determina o menor retângulo delimitador que engloba todos os contornos
    x, y, w, h = cv2.boundingRect(np.vstack(contours))

    # Recorta a imagem com base no retângulo delimitador
    cropped_image = image[y:y+h, x:x+w]

    # Cria o diretório de saída, se necessário
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Salva a imagem recortada
    cv2.imwrite(output_path, cropped_image)
    print(f"A imagem {os.path.basename(image_path)} foi recortada e salva em: {output_path}")

def process_images(input_folder, output_folder):
    # Verifica se o diretório de entrada existe
    if not os.path.isdir(input_folder):
        print(f"Erro: O diretório {input_folder} não foi encontrado.")
        return

    # Itera sobre todos os arquivos na pasta de entrada
    for file_name in os.listdir(input_folder):
        # Verifica se o arquivo é uma imagem (extensões comuns)
        if file_name.lower().endswith((".jpg", ".jpeg")):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            # Recorta a imagem
            crop_whitespace(input_path, output_path)

# Exemplo de uso
if __name__ == "__main__":
    input_directory = escolher_pasta()
    if input_directory:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.join(script_directory, "output_images")
        process_images(input_directory, output_directory)
    else:
        print("Nenhuma pasta foi selecionada.")