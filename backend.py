from flask import Flask, request, jsonify, make_response, send_from_directory
import cv2
import numpy as np
import imutils
import easyocr
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

# # Define upload folder path
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def message():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file:
        # Read the image file
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Preprocess the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #find shapes
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        response = make_response(cv2.imencode('.png', res)[1].tobytes())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='processed_image.png')

        return response
        # Save the processed image to disk
        # processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_image.jpg')
        # cv2.imwrite(processed_image_path, res)

        # Create a Flask response with the encoded image file
        # with open(processed_image_path, 'rb') as f:
        #     content = f.read()
        # response = make_response(content)

        # Set the response headers to indicate that it is a JPG image
        # response.headers.set('Content-Type', 'image/jpg')
        # response.headers.set('Content-Disposition', 'attachment', filename='processed_image.jpg')

        # return response
    
    return jsonify({'error': 'No file uploaded'}), 200

@app.route('/processed_image')
def serve_image():
    # Serve the processed image from the upload folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'processed_image.jpg')

if __name__ == '__main__':
    app.run(debug=True)
    