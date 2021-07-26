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


import datetime
from selfdroid.Constants import Constants
from selfdroid import db


class AppMetadataDBModel(db.Model):
    __tablename__ = "app_metadata"
    __table_args__ = {"sqlite_autoincrement": True}

    # The IDs ARE NOT reusable!
    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    app_name = db.Column(db.String(Constants.DB_APP_NAME_MAX_LENGTH), nullable=False)
    package_name = db.Column(db.String(Constants.DB_PACKAGE_NAME_MAX_LENGTH), unique=True, nullable=False)
    version_code = db.Column(db.Integer(), nullable=False)
    version_name = db.Column(db.String(Constants.DB_VERSION_NAME_MAX_LENGTH), nullable=False)

    min_api_level = db.Column(db.Integer(), nullable=False)
    max_api_level = db.Column(db.Integer(), nullable=True)  # Most apps don't specify their max API level
    apk_file_size = db.Column(db.Integer(), nullable=False)

    added_datetime = db.Column(db.DateTime(), default=datetime.datetime.utcnow, nullable=False)
    last_updated_datetime = db.Column(db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
