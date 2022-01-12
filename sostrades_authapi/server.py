'''
Copyright 2022 Airbus SAS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import sys
import traceback as tb
import logging


from flask import Flask, jsonify
import os.path
from werkzeug.exceptions import HTTPException



# Create  flask server and set local configuration
app = Flask(__name__)

# override debug flag
if '--debugger' in sys.argv:
    app.debug = True

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.DEBUG)

app.logger.info('AuthApi started')

# load & register APIs
from sostrades_authapi.routes import *


# Register exception handler
@app.errorhandler(Exception)
def error_handler(error):
    """
    Standard Error Handler
    """
    tb.print_exc()
    if isinstance(error, HTTPException):
        return jsonify({
            'statusCode': error.code,
            'name': error.name,
            'description': error.description
        }), error.code
    else:
        return jsonify({
            'statusCode': 500,
            'name': 'Internal Server Error',
            'description': str(error)
        }), 500

# Check the presence of environment variables
if os.environ.get('INTERNAL_SSL_CERTIFICATE') is None:
    raise Exception('INTERNAL_SSL_CERTIFICATE environment variable not found')
else:
    app.logger.info('INTERNAL_SSL_CERTIFICATE environment variable found')

if os.environ.get('SAML_V2_METADATA_FOLDER') is None:
    raise Exception('SAML_V2_METADATA_FOLDER environment variable not found')
else:
    app.logger.info('SAML_V2_METADATA_FOLDER environment variable found')

# Check that the settings.json file is present:
settings_json_file = os.environ.get('SAML_V2_METADATA_FOLDER')
if not os.path.exists(settings_json_file):
    raise Exception('SSO settings.json file not found')
else:
    app.logger.info('SSO settings.json file found')

