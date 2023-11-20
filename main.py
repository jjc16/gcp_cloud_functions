import functions_framework
import flask
from google.cloud import kms
import pybase64 as base64

project_id='josh-website-1234'
location_id='us-central1'
# num_bytes=1024
# client = kms.KeyManagementServiceClient()

# location_name = client.common_location_path(project_id, location_id)

# # Call the API.
# protection_level = kms.ProtectionLevel.HSM
# random_bytes_response = client.generate_random_bytes(request={'location': location_name, 'length_bytes': num_bytes, 'protection_level': protection_level})
# b64_num = (base64.b64encode(random_bytes_response.data))

def generate_random_bytes(project_id, location_id, num_bytes):
    """
    Generate random bytes with entropy sourced from the given location.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        num_bytes (integer): number of bytes of random data.

    Returns:
        bytes: Encrypted ciphertext.

    """

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the location name.
    location_name = client.common_location_path(project_id, location_id)

    # Call the API.
    protection_level = kms.ProtectionLevel.HSM
    random_bytes_response = client.generate_random_bytes(request={'location': location_name, 'length_bytes': num_bytes, 'protection_level': protection_level})

    b64_num = (base64.b64encode(random_bytes_response.data))
    print(f'Random bytes: {b64_num}')
    return b64_num


@functions_framework.http
def randomnum(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    try:
        request_json = request.get_json(silent=True)
        request_args = request.args

        response = {}
        if request_json and 'num_bytes' in request_json:
            num_bytes = int(request_json['num_bytes'])
        elif request_args and 'num_bytes' in request_args:
            num_bytes = int(request_args['num_bytes'])
        else:
            num_bytes = 1024

        if num_bytes < 0 or num_bytes > 1024:
            resp = flask.make_response('Error: bytes must be in range [0, 1024]', 400)
            return resp

        bt = generate_random_bytes(project_id, location_id, num_bytes)

        response['base'] = 'base64'
        response['num_bytes'] = str(num_bytes)
        response['random_number'] = str(bt)

        out = flask.make_response(response, 200)
    except:
        flask.make_response('An error occured.', 400)

    return response
        

    #    if request_json and 'name' in request_json:
    #        name = request_json['name']
    #    elif request_args and 'name' in request_args:
    #        name = request_args['name']
    #    else:
    #        name = 'World'
    #    return 'Hello {}!'.format(name)
