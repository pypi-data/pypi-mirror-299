# Python Authentication for FIWARE Data Space (FDSAuth) ![example workflow](https://github.com/CitCom-VRAIN/fdsauth/actions/workflows/package.yml/badge.svg)
Welcome to the **Python Authentication for FIWARE Data Space** repository. This library, or **FDSAuth**, facilitates seamless FIWARE Data Space framework authentication. With built-in support for various authentication protocols and methods, FDSAuth helps developers implement secure and reliable authentication in their applications, ensuring compliance with FIWARE standards and best practices.

## Table of Contents 📚
- [Python Authentication for FIWARE Data Space (FDSAuth) ](#python-authentication-for-fiware-data-space-fdsauth-)
  - [Table of Contents 📚](#table-of-contents-)
  - [Installation 🛠️](#installation-️)
  - [Usage  💻](#usage--)
  - [Development 🚀](#development-)
  - [Contact 📫](#contact-)
  - [Acknowledgments 🙏](#acknowledgments-)

## Installation 🛠️
To install FDSAuth, simply use `pip`:

```bash
pip install fdsauth
```

## Usage  💻
First a DID (Decentralized Identifier) and the corresponding key-material is required. You can create such via:
```bash
mkdir certs && cd certs
docker run -v $(pwd):/cert quay.io/wi_stefan/did-helper:0.1.1
```

Define following environment variables in your `.env` file. Substitute example values for your own:
```bash
export KEYCLOAK_URL="http://keycloak-consumer.127.0.0.1.nip.io:8080"
export DATA_SERVICE_URL="http://mp-data-service.127.0.0.1.nip.io:8080"
export REALM="test-realm"
export CLIENT_ID="admin-cli"
export USERNAME="test-user"
export PASSWORD="test"
export CREDENTIAL_CONFIGURATION_ID="user-credential"
export CREDENTIAL_IDENTIFIER="user-credential"
export PRIVATE_KEY_PATH="./certs/private-key.pem"
export DID_PATH="./certs/did.json"
```

Usage example:
```python
from dotenv import load_dotenv
from fdsauth import Consumer, Provider
import os

# Load environment variables from .env file
load_dotenv()

#Create a Consumer instance and retrieve the auth token
consumer = Consumer(
    keycloak_url=os.getenv("KEYCLOAK_URL"),
    data_service_url=os.getenv("DATA_SERVICE_URL"),
    realm=os.getenv("REALM"),
    client_id=os.getenv("CLIENT_ID"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    credential_configuration_id=os.getenv("CREDENTIAL_CONFIGURATION_ID"),
    credential_identifier=os.getenv("CREDENTIAL_IDENTIFIER"),
    private_key_path=os.getenv("PRIVATE_KEY_PATH"),
    did_path=os.getenv("DID_PATH"),
)
auth_token = consumer.get_auth_token()
```

## Development 🚀
```bash
# Create virtual env
python3 -m venv ./venv && source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build
python setup.py sdist bdist_wheel

# Local testing
pip install dist/fdsauth-X.X.X-py3-none-any.whl
```

## Contact 📫
For any questions or support, please reach out to us via GitHub Issues or email us at [joamoteo@upv.es](mailto:joamoteo@upv.es).

## Acknowledgments 🙏
This work has been made by **VRAIN** for the **CitCom.ai** project, co-funded by the EU.

<img src="https://vrain.upv.es/wp-content/uploads/2022/01/vrain_1920_1185.jpg" alt="VRAIN" width="200"/>
<img src="https://www.fiware.org/wp-content/directories/research-development/images/citcom-ai.png" alt="CitCom.ai" width="200"/>
