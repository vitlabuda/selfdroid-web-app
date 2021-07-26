# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from typing import List, Dict, Any
import os.path
from selfdroid.Settings import Settings


class Constants:
    SELFDROID_WEB_APP_VERSION: float = 1.0

    SUPPORTED_API_VERSIONS: List[int] = [1]

    DATABASE_URI: str = "sqlite:///" + os.path.join(Settings.DATA_DIRECTORY, "database.sqlite")

    TEMPORARY_DIRECTORY: str = os.path.join(Settings.DATA_DIRECTORY, "temp/")
    APKS_DIRECTORY: str = os.path.join(Settings.DATA_DIRECTORY, "apks/")
    ICONS_DIRECTORY: str = os.path.join(Settings.DATA_DIRECTORY, "icons/")
    SECRET_KEY_FILE: str = os.path.join(Settings.DATA_DIRECTORY, "secret_key")
    APP_STORAGE_LOCK_FILE: str = os.path.join(Settings.DATA_DIRECTORY, "app_storage.lock")

    ICON_WIDTH_AND_HEIGHT: int = 192  # An app's icon is always a square PNG image

    DB_APP_NAME_MAX_LENGTH: int = 256
    DB_PACKAGE_NAME_MAX_LENGTH: int = 512
    DB_VERSION_NAME_MAX_LENGTH: int = 32

    FLASH_CATEGORY_SUCCESS: str = "success"
    FLASH_CATEGORY_ERROR: str = "error"
    FLASH_CATEGORY_FORM_ERROR: str = "form_error"

    TALISMAN_OPTIONS: Dict[str, Any] = {
        "force_https": True,
        "strict_transport_security": False,  # HSTS should be set on the internet-facing web server, if needed.
        "frame_options": "DENY",
        "referrer_policy": "same-origin",
        "session_cookie_secure": True,  # This seems not to work (at least when accessing the web app via the Flask development server) -> it's set using app.config too.
        "session_cookie_http_only": True,  # This seems not to work (at least when accessing the web app via the Flask development server) -> it's set using app.config too.
        "force_file_save": True,
        "content_security_policy": {
            "default-src": "'self'",
            "style-src": "'self'",
            "script-src": "'self'",
            "img-src": ["'self'", "data:"],
            "object-src": "'none'",
            "frame-ancestors": "'none'",
            "form-action": "'self'",
            "base-uri": "'none'"
        },
        "content_security_policy_nonce_in": ["script-src", "style-src"]
    }
