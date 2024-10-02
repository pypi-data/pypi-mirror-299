import base64
import json
import requests
import subprocess


class Consumer:
    def __init__(
        self,
        keycloak_url,
        data_service_url,
        realm,
        client_id,
        username,
        password,
        credential_configuration_id,
        credential_identifier,
        private_key_path,
        did_path,
    ):
        self.keycloak_url = keycloak_url
        self.data_service_url = data_service_url
        self.realm = realm
        self.client_id = client_id
        self.username = username
        self.password = password
        self.credential_configuration_id = credential_configuration_id
        self.credential_identifier = credential_identifier
        self.private_key_path = private_key_path
        self.did_path = did_path
        self._access_token = None
        self._credential_access_token = None
        self.holder_did = None
        self.verifiable_credential = None
        self.token_endpoint = None
        self.verifiable_presentation = None
        self.jwt = None
        self.vp_token = None

    @property
    def access_token(self):
        if not self._access_token:
            self._access_token = self._get_access_token()
        return self._access_token

    def _get_access_token(self):
        """Retrieve access token from Keycloak."""
        url = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token"
        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    @property
    def offer_uri(self):
        """Retrieve the offer URI for credential configuration."""
        url = f"{self.keycloak_url}/realms/{self.realm}/protocol/oid4vc/credential-offer-uri"
        params = {"credential_configuration_id": self.credential_configuration_id}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return f"{data['issuer']}{data['nonce']}"

    @property
    def pre_authorized_code(self):
        """Retrieve the pre-authorized code using the offer URI."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(self.offer_uri, headers=headers)
        response.raise_for_status()
        return response.json()["grants"][
            "urn:ietf:params:oauth:grant-type:pre-authorized_code"
        ]["pre-authorized_code"]

    @property
    def credential_access_token(self):
        """Retrieve the credential access token."""
        if not self._credential_access_token:
            self._credential_access_token = self._get_credential_access_token()
        return self._credential_access_token

    def _get_credential_access_token(self):
        """Exchange pre-authorized code for credential access token."""
        url = f"{self.keycloak_url}/realms/{self.realm}/protocol/openid-connect/token"
        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:pre-authorized_code",
            "code": self.pre_authorized_code,
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_verifiable_credential(self):
        """Retrieve the verifiable credential."""
        url = f"{self.keycloak_url}/realms/{self.realm}/protocol/oid4vc/credential"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.credential_access_token}",
        }
        data = json.dumps(
            {"credential_identifier": self.credential_identifier, "format": "jwt_vc"}
        )
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        self.verifiable_credential = response.json()["credential"]
        return self.verifiable_credential

    def get_token_endpoint(self):
        """Retrieve the token endpoint from the data service."""
        url = f"{self.data_service_url}/.well-known/openid-configuration"
        response = requests.get(url)
        response.raise_for_status()
        self.token_endpoint = response.json()["token_endpoint"]
        return self.token_endpoint

    def run_did_helper(self):
        with open(self.did_path, "r") as f:
            did_data = json.load(f)
        self.holder_did = did_data["id"]
        return self.holder_did

    def create_jwt_header(self):
        """Create the JWT header."""
        header = json.dumps({"alg": "ES256", "typ": "JWT", "kid": self.holder_did})
        return base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")

    def create_payload(self):
        """Create the JWT payload."""
        payload = json.dumps(
            {
                "iss": self.holder_did,
                "sub": self.holder_did,
                "vp": self.verifiable_presentation,
            }
        )
        return base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")

    def sign_jwt(self, header, payload):
        """Sign the JWT using the private key."""
        message = f"{header}.{payload}"
        process = subprocess.run(
            ["openssl", "dgst", "-sha256", "-binary", "-sign", self.private_key_path],
            input=message.encode(),
            stdout=subprocess.PIPE,
            check=True,
        )
        return base64.urlsafe_b64encode(process.stdout).decode().rstrip("=")

    def get_vp_token(self):
        """Get the Verifiable Presentation (VP) token."""
        return base64.urlsafe_b64encode(self.jwt.encode()).decode().rstrip("=")

    def get_data_service_access_token(self):
        """Retrieve the data service access token using the VP token."""
        headers = {"Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "vp_token", "vp_token": self.vp_token, "scope": "default"}
        response = requests.post(self.token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        self.data_service_access_token = response.json()["access_token"]
        return response.json()["access_token"]

    def create_verifiable_presentation(self):
        """Create the verifiable presentation."""
        self.verifiable_presentation = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiablePresentation"],
            "verifiableCredential": [self.verifiable_credential],
            "holder": self.holder_did,
        }
        return self.verifiable_presentation

    def generate_jwt(self):
        """Generate the JWT."""
        header = self.create_jwt_header()
        payload = self.create_payload()
        signature = self.sign_jwt(header, payload)
        self.jwt = f"{header}.{payload}.{signature}"
        return self.jwt

    def get_auth_token(self):
        """Execute the main process flow."""
        self.get_verifiable_credential()
        self.get_token_endpoint()
        self.run_did_helper()
        self.create_verifiable_presentation()
        self.generate_jwt()
        self.vp_token = self.get_vp_token()
        self.get_data_service_access_token()

        return self.data_service_access_token
