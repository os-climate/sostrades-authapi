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

from dotenv import load_dotenv
from os.path import join, dirname


if __name__ == '__main__':
    # Load env file
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    from sostrades_authapi import server

    #start the server
    server.app.run(host='0.0.0.0', port=8000, debug=True)
