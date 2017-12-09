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
        emotions.append('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        emotions.append('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        emotions.append('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        emotion["anger"]=likelihood_name[face.anger_likelihood]
        emotion["joy"]=likelihood_name[face.joy_likelihood]
        emotion["surprise"] = likelihood_name[face.surprise_likelihood]
    return emotion

