# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
# SPDX-License-Identifier: Apache-2.0

import os

from google import genai
from google.auth.credentials import Credentials
from google.genai.client import DebugConfig
from google.genai.types import HttpOptions, HttpOptionsDict

from genkit.ai.plugin import Plugin
from genkit.ai.registry import GenkitRegistry
from genkit.plugins.google_genai.models.gemini import GeminiModel, GeminiVersion

PLUGIN_NAME = 'google_genai'


def google_genai_name(name: str) -> str:
    """Create a Google AI action name.

    Args:
        name: Base name for the action.

    Returns:
        The fully qualified Google AI action name.
    """
    return f'{PLUGIN_NAME}/{name}'


class GoogleGenai(Plugin):
    """Google Ai plugin for Firebase Genkit"""

    name = PLUGIN_NAME

    def __init__(
        self,
        vertexai: bool | None = None,
        api_key: str | None = None,
        credentials: Credentials | None = None,
        project: str | None = None,
        location: str | None = None,
        debug_config: DebugConfig | None = None,
        http_options: HttpOptions | HttpOptionsDict | None = None,
    ):
        api_key = api_key if api_key else os.getenv('GEMINI_API_KEY')
        if not vertexai and not api_key:
            raise ValueError(
                'Gemini api key should be passed in plugin params '
                'or as a GEMINI_API_KEY environment variable'
            )
        pass
        self._client = genai.client.Client(
            vertexai=vertexai,
            api_key=api_key if not vertexai else None,
            credentials=credentials,
            project=project,
            location=location,
            debug_config=debug_config,
            http_options=http_options,
        )

    def initialize(self, ai: GenkitRegistry) -> None:
        """Initialize the plugin by registering actions in the registry.

        Args:
            ai: the action registry.

        Returns:
            None
        """

        for version in GeminiVersion:
            gemini_model = GeminiModel(version, self._client, ai)
            ai.define_model(
                name=google_genai_name(version),
                fn=gemini_model.generate,
                metadata=gemini_model.metadata,
            )
