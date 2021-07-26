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
import sqlalchemy.exc
from selfdroid.appstorage.AppMetadata import AppMetadata
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel
from selfdroid.appstorage.AppStorageConsistencyEnsurer import AppStorageConsistencyEnsurer
from selfdroid.appstorage.apk.APKParser import APKParser
from selfdroid.appstorage.apk.ParsedAPK import ParsedAPK
from selfdroid.appstorage.crud.AppAdderException import AppAdderException
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid import db


class AppAdder:
    """
    This class must be instantiated and have its public methods called in a locked context!
    """

    def __init__(self, uploaded_apk_path: str):
        self._uploaded_apk_path: str = uploaded_apk_path

        self._parsed_apk: ParsedAPK = APKParser(self._uploaded_apk_path).parsed_apk

    def add_app_while_locked(self) -> AppMetadata:
        """
        :return: The metadata of the added app.
        """

        try:
            app_metadata =  self._add_app_while_locked_with_exceptions_handled()

        except (sqlalchemy.exc.SQLAlchemyError, OSError):
            db.session.rollback()

            raise AppAdderException("An error occurred while adding the app!")

        finally:
            AppStorageConsistencyEnsurer().ensure_consistency_while_locked()

        return app_metadata

    def _add_app_while_locked_with_exceptions_handled(self) -> AppMetadata:
        self._check_if_app_can_be_added()

        return self._perform_app_addition()

    def _check_if_app_can_be_added(self) -> None:
        an_app_with_the_same_package_name = AppMetadataDBModel.query.filter_by(package_name=self._parsed_apk.package_name).first()
        if an_app_with_the_same_package_name is not None:
            html_message = WebStatusMessageCollector.format_html_message("An app with the same package name <i>({})</i> is already present on the server! You should update the app instead of adding it!", self._parsed_apk.package_name)
            raise AppAdderException(html_message)

    def _perform_app_addition(self) -> AppMetadata:
        # An UserReadableException mustn't be raised in this method!

        # 1. Database
        db_model = self._parsed_apk.create_new_db_model_with_metadata()
        db.session.add(db_model)
        db.session.commit()

        assert isinstance(db_model.id, int)

        app_metadata = AppMetadata.from_db_model(db_model)

        # 2. APK
        apk_path = app_metadata.get_apk_path()

        os.rename(self._uploaded_apk_path, apk_path)

        # 3. Icon
        icon_path = app_metadata.get_icon_path()

        with open(icon_path, "wb") as icon_file:
            icon_file.write(self._parsed_apk.uniform_png_app_icon)

        return app_metadata
