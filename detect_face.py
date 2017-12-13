import argparse
import io

from google.cloud import vision
from google.cloud.vision import types


def detect_faces(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    emotion = {}
    emotions=[]

    for face in faces:
        emotion["anger"]=likelihood_name[face.anger_likelihood]
        emotion["joy"]=likelihood_name[face.joy_likelihood]
        emotion["surprise"] = likelihood_name[face.surprise_likelihood]
        emotion["blurred"] = likelihood_name[face.blurred_likelihood]
        emotion["headwear"] = likelihood_name[face.headwear_likelihood]
    return emotion

