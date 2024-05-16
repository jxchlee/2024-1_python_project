# 5.16 머신러닝 작동하는 것 확인. 작동을 위해 맞는 버전 설치가 필요함(파이썬 3.8-3.11, tensorflow 2.12. 텐서플로우는 12만 되는 것은 아니라고는 하는데 일단 최신 버전인 16에서는 안되는 것 같음)
# src 폴더에 넣어놓은 내 사진으로 테스트를 해본 결과 class 1 이미지를 결과로 가져가는 것을 확인하였음. 나는 class 2라서 잘못된 결과가 나오는 상황.
# 다음 모델을 만들 땐 class1에 검은 화면같이 default 화면을 하나 넣어 놓고 학습 사키는 것이 좋을 것 같음.
# 일단 기능 확인을 위해 이미지로 결과를 출력하였지만 후에 실시간 얼굴인식을 위해 카메라 모듈을 사용할 예정

from tensorflow import keras
# from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os
model_route = os.path.abspath('../../model/keras_model.h5')
label_route = os.path.abspath('../../model/labels.txt')
image_route = os.path.abspath('../../src/testImage.jpg')
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
print(model_route)
# Load the model
# model = load_model("keras_Model.h5", compile=False)
model = keras.models.load_model(model_route, compile=False)
# Load the labels
class_names = open(label_route, "r").readlines()

print(model, class_names)
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open(image_route).convert("RGB")

# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Print prediction and confidence score
print("Class:", class_name[2:], end="")
print("Confidence Score:", confidence_score)
