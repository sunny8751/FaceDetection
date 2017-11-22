import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

def detect(url, subscription_key, subscription_location):
    uri_base = 'https://' + subscription_location + '.api.cognitive.microsoft.com'

    # Request headers.
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # Body. The URL of a JPEG image to analyze.
    body = {'url': url}

    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)

        print ('Response:')
        parsed = json.loads(response.text)
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        return parsed

    except Exception as e:
        print('Error:')
        print(e)
