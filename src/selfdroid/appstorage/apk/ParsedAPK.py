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
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel


class ParsedAPK:
    def __init__(self,
                 app_name: str, package_name: str, version_code: int, version_name: str,
                 min_api_level: int, max_api_level: Optional[int],
                 apk_file_size: int, uniform_png_app_icon: bytes):

        self.app_name: str = app_name
        self.package_name: str = package_name
        self.version_code: int = version_code
        self.version_name: str = version_name

        self.min_api_level: int = min_api_level
        self.max_api_level: Optional[int] = max_api_level

        self.apk_file_size: int = apk_file_size
        self.uniform_png_app_icon: bytes = uniform_png_app_icon

    def create_new_db_model_with_metadata(self) -> AppMetadataDBModel:
        return AppMetadataDBModel(
            app_name=self.app_name,
            package_name=self.package_name,
            version_code=self.version_code,
            version_name=self.version_name,

            min_api_level=self.min_api_level,
            max_api_level=self.max_api_level,

            apk_file_size=self.apk_file_size
        )

    def fill_existing_db_model_with_metadata(self, db_model: AppMetadataDBModel) -> None:
        db_model.app_name = self.app_name
        db_model.package_name = self.package_name
        db_model.version_code = self.version_code
        db_model.version_name = self.version_name

        db_model.min_api_level = self.min_api_level
        db_model.max_api_level = self.max_api_level

        db_model.apk_file_size = self.apk_file_size
