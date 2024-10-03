#Importando biblioteca necessária

from skimage.io import imread, imsave

#Função para leitura da imagem
def read_image(path, is_gray = False):
    image = imread(path, as_gray = is_gray)
    
    return image

#Função para salvar imagem
def save_image(image, path):
    imsave(path, image)