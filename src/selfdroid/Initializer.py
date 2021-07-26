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


import os
import os.path
import secrets
from selfdroid.Constants import Constants
from selfdroid.Settings import Settings


class Initializer:
    _SECRET_KEY_LENGTH: int = 64

    def initialize_data_directory(self) -> None:
        if not os.path.isfile(Settings.DATA_DIRECTORY):
            os.makedirs(Settings.DATA_DIRECTORY, exist_ok=True)
            os.chmod(Settings.DATA_DIRECTORY, 0o700)

        if not os.path.isdir(Constants.TEMPORARY_DIRECTORY):
            os.mkdir(Constants.TEMPORARY_DIRECTORY)

        if not os.path.isdir(Constants.APKS_DIRECTORY):
            os.mkdir(Constants.APKS_DIRECTORY)

        if not os.path.isdir(Constants.ICONS_DIRECTORY):
            os.mkdir(Constants.ICONS_DIRECTORY)

        if not os.path.isfile(Constants.SECRET_KEY_FILE):
            new_secret_key = secrets.token_bytes(Initializer._SECRET_KEY_LENGTH)
            with open(Constants.SECRET_KEY_FILE, "wb") as file:
                os.chmod(Constants.SECRET_KEY_FILE, 0o600)
                file.write(new_secret_key)

    def get_secret_key(self) -> bytes:
        with open(Constants.SECRET_KEY_FILE, "rb") as file:
            return file.read()
