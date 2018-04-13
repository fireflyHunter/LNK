import keras
import numpy as np
from keras.applications import vgg16, inception_v3, resnet50, mobilenet
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions

# Load the VGG model
vgg_model = vgg16.VGG16(weights='imagenet')
vgg_model.summary()

filename = '../vtt2016/images/{}_{}f.jpg'.format(1109,9)
# load an image in PIL format
original = load_img(filename, target_size=(224, 224))
print('PIL image size', original.size)


# convert the PIL image to a numpy array
# IN PIL - image is in (width, height, channel)
# In Numpy - image is in (height, width, channel)
numpy_image = img_to_array(original)
image_batch = np.expand_dims(numpy_image, axis=0)
processed_image = vgg16.preprocess_input(image_batch.copy())

# get the predicted probabilities for each class
predictions = vgg_model.predict(processed_image)
# print predictions

# convert the probabilities to class labels
# We will get top 5 predictions which is the default
label = decode_predictions(predictions)
print(label)