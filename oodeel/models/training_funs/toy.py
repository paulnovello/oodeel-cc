from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf


def train_convnet(
    train_data: tf.data.Dataset, 
    batch_size: int = 128, 
    epochs: int = 5
) -> tf.keras.Model:
    
    classes = train_data.map(lambda x, y: y).unique()
    num_classes=len(list(classes.as_numpy_iterator()))

    train_data = train_data.map(lambda x, y: (x, tf.one_hot(y, num_classes))).batch(batch_size)
    model = keras.Sequential(
        [
            #keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    # compile and fit
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(train_data, epochs=epochs)    

    return model

