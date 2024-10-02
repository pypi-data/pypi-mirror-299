# Copyright 2023 Specter Ops, Inc.
#
# Licensed under the Apache License, Version 2.0
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0import base64

import datetime
import hashlib
import hmac
import base64
from typing import Optional

import httpx
from httpx import URL, Headers

from blood_hound_api_client import AuthenticatedClient


class HMACAuth(httpx.Auth):
    def __init__(self, api_token: str, api_token_id: str):
        self.token_key = api_token
        self.token_id = api_token_id

    def auth_flow(self, request: httpx.Request):
        # Extract method, URL, headers, and body from the request
        method = request.method
        url = str(request.url)
        body = request.content or b''

        request.headers.update(self._sign_request(method, request.url, body))

        # Yield the signed request
        yield request

    def _sign_request(self, method: str, uri: URL, body: Optional[bytes] = None) -> dict:
        """
        Create the HMAC signature chain and return the signed headers.
        """
        # Step 1: Create the HMAC digester for the token key
        digester = hmac.new(self.token_key.encode('utf-8'), digestmod=hashlib.sha256)

        operation_key = f'{method}{uri.path}'.encode('utf-8')
        # Step 2: Create the OperationKey by updating the method and uri
        digester.update(f'{method}{uri.path}'.encode('utf-8'))

        # Step 3: Update the digester for further chaining with the first HMAC digest link
        digester = hmac.new(digester.digest(), digestmod=hashlib.sha256)

        # Step 4: Get the current datetime formatted as RFC3339 and to the hour
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        # Format the datetime to RFC 3339 format with a 'Z' for UTC
        datetime_formatted = now.isoformat(timespec='seconds').replace('+00:00', 'Z')
        datetime_signed = datetime_formatted[:13].encode('utf-8')
        digester.update(datetime_formatted[:13].encode('utf-8'))

        # Step 5: Update the digester again for chaining the second HMAC digest link
        digester = hmac.new(digester.digest(), digestmod=hashlib.sha256)

        # Step 6: If the request has a body, update the digester with the body content
        if body is not None:
            digester.update(body)

        # Step 7: Generate the final signature
        signature = base64.b64encode(digester.digest()).decode('utf-8')

        # Step 8: Create headers including the signature, token ID, and date
        headers = {
            'User-Agent': 'bhe-python-sdk 0001',
            'Authorization': f'bhesignature {self.token_id}',
            'RequestDate': datetime_formatted,
            'Signature': signature,
            # 'Content-Type': 'application/json',
        }

        return headers

    def _generate_signature(self, method: str, url: str, body: bytes) -> str:
        # Prepare data to sign (method, URL, and body)
        message = f"{method.upper()} {url}\n{body.decode('utf-8')}"

        # Generate HMAC signature using the API token as the key
        hmac_digest = hmac.new(
            self.api_token.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()

        # Encode the signature as a base64 string
        return base64.b64encode(hmac_digest).decode('utf-8')

class HMACAuthenticatedClient(AuthenticatedClient):
    def __init__(self, base_url: str, token_key: str, token_id: str):
        super().__init__(base_url=base_url, token=token_key)
        self.token = token_key
        self.prefix = ""
        self.token_key = token_key
        self.token_id = token_id
        self.auth = HMACAuth(api_token=self.token_key, api_token_id=self.token_id)

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        mounts = {
            "all://bloodhound.localhost": httpx.HTTPTransport(proxy="http://localhost"),
        }
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                mounts=mounts,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                auth=self.auth,
                **self._httpx_args,
            )
        return self._client

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            mounts = {
                "all://bloodhound.localhost": httpx.AsyncHTTPTransport(proxy="http://localhost"),
            }
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                mounts=mounts,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                auth=self.auth,
                **self._httpx_args,
            )
        return self._async_client


