#! /usr/bin/env python3
import streamlit as st
import io
import numpy as np
from PIL import Image
import tensorflow as tf
import efficientnet.tfkeras as efn

# Title and Description
st.title("Plant Disease Detection")
st.write("Just upload your plant's leaf image and get predictions if your plant is healthy or not!")
st.write("")


gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

# Loading Model
model = tf.keras.models.load_model("model.h5")

# File Uploader
uploaded_file = st.file_uploader("Choose your plant leaf image", type=['png','jpg'])

predictions_map = {0: "is healthy", 1: "has multiple diseases", 2: "has Rust", 3: "has Scab"}

if uploaded_file is not None:

    #image = Image.open(io.BytesIO(uploaded_file.read()))
    image = Image.open(io.BytesIO(uploaded_file.read()))

    st.image(image, use_column_width=True)

    # Resize and convert to numpy array of (0,1)
    resized_image = np.array(image.resize((512, 512)))/255.
    # Add batch dimension
    image_batch = resized_image[np.newaxis, :, :, :]
    # Get the predictions from the model
    predictions_arr = model.predict(image_batch)

    predictions = np.argmax(predictions_arr)

    result_text = f"The plant leaf {predictions_map[predictions]} with {int(predictions_arr[0][predictions] * 100)}% probability."

    if predictions == 0:
        st.success(result_text)
    else:
        st.error(result_text)
