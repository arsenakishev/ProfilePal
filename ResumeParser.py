#Imran Ahmed
#ProfilePal
#This is to parse the resume.
#pip install zeep
#pip install lxml
#pip install xmltodict

from os import listdir
from os.path import isfile, join
from zeep import Client
import xmltodict, json
import Converter

# PURPOSE :: TO HELP SPEED UP PROCESS OF RESUME PARSING USING PYTHON.
def parseResume(fileName, filePath):
    print "Starting Importer... one moment. "
    print ""
    print "Shaking hands with clients..."
    print "-----------------------------"

    # load in the file.
    print "--> Loading Temporary File"
    if(fileName.split('.')[1] != 'txt'):
        toReturn = Converter.document_to_text(fileName, filePath)
        return (toReturn)
    with open(filePath, 'r') as content_file:
        file_contents = content_file.read()  # read the file
        file_name = "resume.doc"  # get from your own processing.

        print "--> LOADED"

        print "--> Connecting to Parser"

        client = Client('http://www.cvparseapi.com/cvparseapi.asmx?WSDL')
        big_endpoint = "http://www.cvparseapi.com/cvparseapi.asmx?WSDL"
        big_key = "f8100053-6dc2-e711-910e-00155d692ee1"
        big_pass = "designproject"

        result = client.service.ParseResumeNTG(f=file_contents, fileName=file_name, YourKey=big_key, Password=big_pass)

        print "--> Connected Passing Data :: Parsing.... (waiting)"

        o = xmltodict.parse(result)
        json_data = json.dumps(o)
        # now we need to parse the xml.
        print "--> DONE:: Next steps do stuff with data received ."
        return (json_data)


