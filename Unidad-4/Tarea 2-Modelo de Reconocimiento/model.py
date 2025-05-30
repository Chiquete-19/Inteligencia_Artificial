import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix, classification_report

class EmotionModelTrainer:
    def __init__(self):
        self.img_size = 100
        self.batch_size = 32
        self.epochs = 15
        self.train_dir = 'DATASET/train'
        self.test_dir = 'DATASET/test'
        self.model = None
        self.history = None

    def setup_data_generators(self):
        train_datagen = ImageDataGenerator(rescale=1./255)
        test_datagen = ImageDataGenerator(rescale=1./255)

        self.train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            color_mode='grayscale',
            class_mode='categorical'
        )

        self.test_generator = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            color_mode='grayscale',
            class_mode='categorical',
            shuffle=False
        )

    def build_model(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
            MaxPooling2D(2, 2),

            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),

            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),

            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),

            Dense(self.train_generator.num_classes, activation='softmax')
        ])

        self.model.compile(
            optimizer=Adam(),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    def train_model(self):
        self.history = self.model.fit(
            self.train_generator,
            epochs=self.epochs,
            validation_data=self.test_generator
        )
        self.model.save("modelo_emociones.h5")

    def evaluate_model(self):
        Y_pred = self.model.predict(
            self.test_generator,
            steps=self.test_generator.samples // self.test_generator.batch_size + 1
        )
        y_pred = np.argmax(Y_pred, axis=1)
        y_true = self.test_generator.classes

        target_names = list(self.test_generator.class_indices.keys())

        cm = confusion_matrix(y_true, y_pred)
        print("Reporte de clasificación:")
        print(classification_report(y_true, y_pred, target_names=target_names))
        self.plot_confusion_matrix(cm, target_names)

    def run(self):
        self.setup_data_generators()
        self.build_model()
        self.train_model()
        self.evaluate_model()

if __name__ == "__main__":
    trainer = EmotionModelTrainer()
    trainer.run()