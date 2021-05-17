#Original model construction and training file

import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

dir_path = r"C:\Users\dpb24\OneDrive - University of Waterloo\SideProjects\SetGame\Images"
val_dir_path = r"C:\Users\dpb24\OneDrive - University of Waterloo\SideProjects\SetGame\TestingImages"

batch_size = 32
img_height = 31
img_width = 50

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  dir_path,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  val_dir_path,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

print(train_ds.class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = 82

data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomTranslation(0.05, 0.05),
    layers.experimental.preprocessing.RandomZoom(0.05),
  ]
)

# model = Sequential([
#   layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
#   data_augmentation,
#   layers.Conv2D(16, 2, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Conv2D(32, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Conv2D(64, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Dropout(0.2),
#   layers.Flatten(),
#   layers.Dense(328, activation='relu'),
#   layers.Dense(num_classes)
# ])



# model.compile(optimizer='adam',
#               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])

# model.summary()

model = keras.models.load_model('DarkModeSet-1.2')

epochs=5
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


model.save("DarkModeSet-1.2")