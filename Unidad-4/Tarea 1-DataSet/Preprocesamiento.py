import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Función para simular desenfoque mediante redimensionamiento
def blur_image(img):
    img = tf.image.resize(img, [16, 16]) 
    img = tf.image.resize(img, [100, 100])  
    return img

# Crea un generador de datos con aumentos
train_datagen = ImageDataGenerator(
    rescale=1./255,
    brightness_range=[0.8, 1.2],  
    rotation_range=15,            
    horizontal_flip=True,         
    preprocessing_function=blur_image  
)

train_generator = train_datagen.flow_from_directory(
    'archive\\DATASET\\train',
    target_size=(100, 100),
    batch_size=32,
    class_mode='categorical'
)