import os
import tensorflow as tf
from django.conf import settings
from django.shortcuts import render
from PIL import Image
import numpy as np
import openpyxl
from .forms import DigitUploadForm

# Load the model when the server starts
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'digit_entry', 'models', 'mnist_cnn_model.h5')
    model = tf.keras.models.load_model(model_path)
    return model

model = load_model()

def predict_digit(image):
    # Convert image to grayscale and resize it to 28x28
    image = image.convert('L')
    image = image.resize((28, 28))
    image_array = np.array(image).reshape(1, 28, 28, 1) / 255.0
    
    # Make prediction
    prediction = model.predict(image_array)
    predicted_digit = np.argmax(prediction)
    return predicted_digit

def index(request):
    predicted_digit = None

    if request.method == 'POST':
        form = DigitUploadForm(request.POST, request.FILES)
        if form.is_valid():
            digit_image = form.cleaned_data['digit_image']
            image = Image.open(digit_image)
            predicted_digit = predict_digit(image)

            # Define the path for the Excel file where digits will be saved
            file_path = os.path.join(settings.MEDIA_ROOT, 'digits.xlsx')
            if not os.path.exists(file_path):
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(["Digits"])
            else:
                wb = openpyxl.load_workbook(file_path)
                ws = wb.active

            # Append the predicted digit to the Excel sheet
            ws.append([predicted_digit])
            wb.save(file_path)

    else:
        form = DigitUploadForm()

    return render(request, 'digit_entry/index.html', {'form': form, 'predicted_digit': predicted_digit})
