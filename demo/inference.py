import urllib.request
import json
import os
import ssl
import cv2

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

img = cv2.imread("data/n02085782_17.jpg")
img = cv2.resize(img, (224, 224))
img = img.reshape(1, 3, 224, 224).astype('float32')
img = img.tolist()


data = {"input_data": img}


body = str.encode(json.dumps(data))

url = 'https://dogs-classifier-online2.eastus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'F4w6ESUIBr7D7aRV8MzfGe6tHoKbf1hp'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'dogs-online-dp' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    # Convert bytes to string
    result_str = result.decode('utf-8')

    # Convert string to list
    result_list = list(eval(result_str))[0]
    print(result_list)
    
    max_value = max(result_list)
    print("Predict Value:", max_value)
    
    max_index = result_list.index(max_value)
    
    print("Predict Class:", max_index)
    
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
