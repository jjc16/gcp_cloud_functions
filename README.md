# gcp_cloud_functions
This is a catchall for my cloud function code on gcp

## Random number generator

Can also invoke with https://us-central1-josh-website-1234.cloudfunctions.net/random-number-generator

You can change the number of bytes returned by passing the parameter in the URL args:
- https://us-central1-josh-website-1234.cloudfunctions.net/random-number-generator?num_bytes=16

The data can also be passed as a JSON
- {"num_bytes": "16"}


