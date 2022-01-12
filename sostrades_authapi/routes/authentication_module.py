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
"""
Login/logout APIs
"""
import os
import json
from flask import request, make_response, Response, redirect

from sostrades_authapi.server import app
from werkzeug.exceptions import BadRequest, Unauthorized, HTTPException
import requests
import urllib
from urllib.parse import urlparse, urlencode
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from flask.json import jsonify


app.logger.info('Authentication module loaded')

import sostrades_authapi

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.environ.get('SAML_V2_METADATA_FOLDER'))
    return auth


def prepare_flask_request(req):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    url_data = urlparse(req.url)
    return {
        'https': 'on' if req.scheme == 'https' else 'off',
        'http_host': req.host,
        'server_port': url_data.port,
        'script_name': req.path,
        'get_data': req.args.copy(),
        'post_data': req.form.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'query_string': req.query_string
    }


@app.route('/saml/acs', methods=['POST'])
def saml_acs():
    """ one login assertion consumer service based on SAML V2 protocol
    """
    app.logger.debug('ACS request incoming')
    ssl_path = os.environ.get('INTERNAL_SSL_CERTIFICATE')

    req = prepare_flask_request(request)
    auth = init_saml_auth(req)

    auth.process_response()

    if not auth.is_authenticated():
        return Unauthorized('User not authenticated')

    if 'RelayState' in request.form and request.host_url != request.form['RelayState']:
        app.logger.debug(f'Relay found : {request.form["RelayState"]}')

        relay = request.form["RelayState"]
        app.logger.debug(f'method  : {request.method}')
        app.logger.debug(
            f'New relay  : {request.url.replace(request.host_url, relay)}')

        data = {'SAMLResponse': request.form['SAMLResponse'],
                'Redirect': 'False'}
        try:
            resp = requests.request(
                method=request.method,
                url=request.url.replace(request.host_url, relay),
                data=data, verify=ssl_path)

            if resp.status_code == 200:
                app.logger.debug(f'Response content: {resp.json()}')
                return redirect(resp.json()['Redirect_url'])
            else:
                return HTTPException(resp.json())

        except Exception as ex:
            app.logger.exception(ex)
            return HTTPException(ex)
    else:
        return BadRequest('Invalid request "RelayState" parameter is missing')


@app.route('/saml/metadata/', methods=['GET'])
def saml_metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp
