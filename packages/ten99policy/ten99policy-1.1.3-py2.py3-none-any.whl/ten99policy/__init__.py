from __future__ import absolute_import, division, print_function

# Configuration variables

client_id = None
api_base = "http://localhost:5000"
api_key = "t9sk_test_c6a100e0-88b2-4548-a9ca-d4b681503946"
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
max_network_retries = 0
environment = "production"

# Set to either 'debug' or 'info', controls console logging
log = "debug"

# API resources
from ten99policy.api_resources import *  # noqa
