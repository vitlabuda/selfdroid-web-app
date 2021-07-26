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


from typing import Optional
import os.path
import io
import re
import PIL.Image
import pyaxmlparser
from selfdroid.Constants import Constants
from selfdroid.appstorage.apk.ParsedAPK import ParsedAPK
from selfdroid.appstorage.apk.APKParserException import APKParserException


class APKParser:
    class _InvalidAPKMetadataException(Exception):
        # For this class's internal use
        pass

    def __init__(self, apk_path: str):
        try:
            self._apk: pyaxmlparser.APK = pyaxmlparser.APK(apk_path)
            is_valid_apk = self._apk.is_valid_APK()
        except Exception:
            raise APKParserException("Failed to parse the supplied APK file!")

        if not is_valid_apk:
            raise APKParserException("The supplied APK file is not valid!")

        try:
            app_name: str = self._get_and_validate_app_name()
            package_name: str = self._get_and_validate_package_name()
            version_code: int = self._get_and_validate_version_code()
            version_name: str = self._get_and_validate_version_name()

            min_api_level: int = self._get_and_validate_min_api_level()
            max_api_level: Optional[int] = self._get_and_validate_max_api_level()

        except Exception:
            raise APKParserException("Failed to extract the app's metadata from the supplied APK file!")

        try:
            apk_file_size: int = os.path.getsize(apk_path)
        except OSError:
            # This should not happen under normal circumstances
            raise APKParserException("Failed to get the supplied APK's size!")

        try:
            uniform_png_app_icon: bytes = self._get_and_convert_app_icon_to_uniform_png()
        except Exception:
            raise APKParserException("Failed to extract the app's icon from the supplied APK file!")

        self.parsed_apk: ParsedAPK = ParsedAPK(app_name, package_name, version_code, version_name, min_api_level, max_api_level, apk_file_size, uniform_png_app_icon)

    def _get_and_validate_app_name(self) -> str:
        app_name = self._apk.get_app_name()
        if not isinstance(app_name, str):
            raise APKParser._InvalidAPKMetadataException()

        app_name = app_name.strip()
        if not app_name or len(app_name) > Constants.DB_APP_NAME_MAX_LENGTH:
            raise APKParser._InvalidAPKMetadataException()

        return app_name

    def _get_and_validate_package_name(self) -> str:
        package_name = self._apk.packagename
        if not isinstance(package_name, str):
            raise APKParser._InvalidAPKMetadataException()

        package_name = package_name.strip()
        if not package_name or len(package_name) > Constants.DB_PACKAGE_NAME_MAX_LENGTH:
            raise APKParser._InvalidAPKMetadataException()

        if not re.match(r'^[A-Za-z_][0-9A-Za-z._]+[0-9A-Za-z_]$', package_name):
            raise APKParser._InvalidAPKMetadataException()

        return package_name

    def _get_and_validate_version_code(self) -> int:
        version_code = self._apk.version_code
        try:
            version_code = int(version_code)
        except ValueError:
            raise APKParser._InvalidAPKMetadataException()

        if version_code < 1:
            raise APKParser._InvalidAPKMetadataException()

        return version_code

    def _get_and_validate_version_name(self) -> str:
        version_name = self._apk.version_name
        if not isinstance(version_name, str):
            raise APKParser._InvalidAPKMetadataException()

        version_name = version_name.strip()
        if not version_name or len(version_name) > Constants.DB_VERSION_NAME_MAX_LENGTH:
            raise APKParser._InvalidAPKMetadataException()

        return version_name

    def _get_and_validate_min_api_level(self) -> int:
        # Technically, apps don't have to specify this attribute, but in practice, "every" app has it
        min_api_level = self._apk.get_min_sdk_version()
        try:
            min_api_level = int(min_api_level)
        except ValueError:
            raise APKParser._InvalidAPKMetadataException()

        if min_api_level < 1:
            raise APKParser._InvalidAPKMetadataException()

        return min_api_level

    def _get_and_validate_max_api_level(self) -> Optional[int]:
        # Apps can specify this attribute, but in practice, "no" apps have it, as it unnecessarily blocks forward compatibility
        max_api_level = self._apk.get_max_sdk_version()
        if max_api_level is None:
            return None

        try:
            max_api_level = int(max_api_level)
        except ValueError:
            raise APKParser._InvalidAPKMetadataException()

        if max_api_level < 1:
            raise APKParser._InvalidAPKMetadataException()

        return max_api_level

    def _get_and_convert_app_icon_to_uniform_png(self) -> bytes:
        original_app_icon_data = self._apk.get_file(self._apk.get_app_icon(640))

        # If the DPI is not specified, an "anydpi" vector icon (in XML format) is usually returned which cannot be parsed
        with io.BytesIO(original_app_icon_data) as original_app_icon_bytes_io:
            image = PIL.Image.open(original_app_icon_bytes_io)

            image = image.convert("RGBA")

        image = image.resize((Constants.ICON_WIDTH_AND_HEIGHT, Constants.ICON_WIDTH_AND_HEIGHT))

        with io.BytesIO() as uniform_png_icon_bytes_io:
            image.save(uniform_png_icon_bytes_io, format="PNG")

            return uniform_png_icon_bytes_io.getvalue()
