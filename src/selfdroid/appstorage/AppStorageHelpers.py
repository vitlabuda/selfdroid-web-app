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


import string
import os.path
from flockbasedlock.flockbasedlock import FlockBasedLock
from selfdroid.Constants import Constants
from selfdroid.Helpers import Helpers


class AppStorageHelpers:
    _TEMPORARY_FILENAME_CHARACTER_SET: str = string.digits + string.ascii_lowercase
    _TEMPORARY_FILENAME_LENGTH: int = 32

    @staticmethod
    def get_app_storage_lock() -> FlockBasedLock:
        return FlockBasedLock(Constants.APP_STORAGE_LOCK_FILE, single_use=True)

    @classmethod
    def get_apk_path_by_app_id(cls, app_id: int) -> str:
        return os.path.join(Constants.APKS_DIRECTORY, cls.get_apk_filename_by_app_id(app_id))

    @staticmethod
    def get_apk_filename_by_app_id(app_id: int) -> str:
        return "{}.apk".format(app_id)

    @classmethod
    def get_icon_path_by_app_id(cls, app_id: int) -> str:
        return os.path.join(Constants.ICONS_DIRECTORY, cls.get_icon_filename_by_app_id(app_id))

    @staticmethod
    def get_icon_filename_by_app_id(app_id: int) -> str:
        return "{}.png".format(app_id)

    @classmethod
    def generate_temp_filepath_for_apk_while_locked(cls) -> str:
        while True:
            random_string = Helpers.generate_secure_random_string(cls._TEMPORARY_FILENAME_CHARACTER_SET, cls._TEMPORARY_FILENAME_LENGTH)

            path = os.path.join(Constants.TEMPORARY_DIRECTORY, "{}.apk".format(random_string))
            if not os.path.exists(path):
                return path
