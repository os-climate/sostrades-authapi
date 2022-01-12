# SoStrades authAPI

This is the repo for the SoSTrades Authentication API.

##How it works
  When a user logs in SoSTrades Application, if the CORP SSO authentication succeeded, it redirects to this SoSTrades Authentication server.
The SoSTrades Authentication server drives CORP SSO request to the SoSTrades API server. 
The SoSTrades API server manages user authentication then responds to the SoSTrades Authentication API with access information.
The SoSTrades Authentication API, then, redirects the browser to the SoSTrades Application.

The authentication protocol used in SoSTrades is SAML v2.

## Packages installation
### Online (no vpn) install
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org 

## Configuration
- set the SAML v2 'settings.json' file for the SSO authentication (the file must have this name 'settings.json')
A template of this file is located in the 'sostrades_authapi\configuration_template\saml' folder.
All explanations on how to fill it are accessible here: https://github.com/onelogin/python3-saml.
- in the '.env' file, set the environment variable SAML_V2_METADATA_FOLDER with the folder path where the settings.json is
- in the '.env' file, set the environment variable INTERNAL_SSL_CERTIFICATE with the certificate file path. 
This certificate is used to send a request to the SoSTrades API server via SSL verification.
- in the '.flaskenv' file, set the path to the sostrades_authapi\server.py file in the variable FLASK_APP

## API Start
If you want to run the authAPI locally:
python \sostrades_authapi\sostrades_authapi.py

