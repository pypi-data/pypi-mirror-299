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

import asyncio
import auth
from auth.hmac_authenticated_client import HMACAuthenticatedClient

from blood_hound_api_client import AuthenticatedClient
from blood_hound_api_client.api.api_info import get_api_version
from blood_hound_api_client.models import GetApiVersionResponse200

async def get_version_async(base_url, token_key, token_id):
    hmac_authenticated_client = HMACAuthenticatedClient(base_url=base_url, token_key=token_key, token_id=token_id)
    client = hmac_authenticated_client

    async with client as client:
        version: GetApiVersionResponse200 = await get_api_version.asyncio(client=client)
        response: Response[GetApiVersionResponse200] = await get_api_version.asyncio_detailed(client=client)
        print(f"async version: {version.data}")
        print(f"async response: {response}")

def get_version(base_url, token_key, token_id):
    hmac_authenticated_client = HMACAuthenticatedClient(base_url=base_url, token_key=token_key, token_id=token_id)
    client = hmac_authenticated_client

    with client as client:
        version: GetApiVersionResponse200 = get_api_version.sync(client=client)
        response: Response[GetApiVersionResponse200] = get_api_version.sync_detailed(client=client)
        print(f"version {version.data}")
        print(f"resopnse {response}")

if __name__ == '__main__':
    token_key = "CAuAwLgPag3xpjfx5gYt3mEpRpK5DXkL1LGVK+utqMLTnlakVmjeZw==" # Use your API token key
    token_id = "5f538a38-fd90-4228-b17b-ee09056c6ade"                      # Use your API token id
    get_version("http://bloodhound.localhost", token_key, token_id)
    asyncio.run(get_version_async("http://bloodhound.localhost", token_key, token_id))
