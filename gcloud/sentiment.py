import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def return_results(annotations):
    score = annotations.document_sentiment.score
#    magnitude = annotations.document_sentiment.magnitude
    sentiment_list = []
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        sentiment_list.append(sentence_sentiment)
#        print('Sentence {} has a sentiment score of {}'.format(
#            index, sentence_sentiment))

#    print('Overall Sentiment: score of {} with magnitude of {}'.format(
#        score, magnitude))
    return sentiment_list 


def analyze(filename):
    client = language.LanguageServiceClient()

    with open(filename, 'r') as review_file:
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    return return_results(annotations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()

    analyze(args.filename)
