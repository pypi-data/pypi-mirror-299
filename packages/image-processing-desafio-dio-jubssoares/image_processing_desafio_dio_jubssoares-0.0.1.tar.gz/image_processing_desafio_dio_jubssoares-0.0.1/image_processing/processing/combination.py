#Importando bibliotecas necessárias

import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

#Função para encontrar a diferença
def find_difference(image_1, image_2):
    assert image_1.shape == image_2.shape, "Specify 2 images with de same shape."
    
    gray_image_1 = rgb2gray(image_1)
    gray_image_2 = rgb2gray(image_2)
    
    (score, differnce_image) = structural_similarity(gray_image_1, gray_image_2, full = True)
    
    print(f"Similarity of the images: {score}.")
    
    normalized_difference_image = (differnce_image - np.min(differnce_image)) / (np.max(differnce_image) - np.min(differnce_image))
    
    return normalized_difference_image

#Função para o histograma de cores em comum
def transfer_histogram(image_1, image_2):
    matched_image = match_histograms(image_1, image_2, multichannel = True)
    
    return matched_image