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


from typing import Tuple
import os
import sqlalchemy.exc
from selfdroid.UserReadableException import UserReadableException
from selfdroid.appstorage.AppMetadata import AppMetadata
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel
from selfdroid.appstorage.AppStorageConsistencyEnsurer import AppStorageConsistencyEnsurer
from selfdroid.appstorage.apk.APKParser import APKParser
from selfdroid.appstorage.apk.ParsedAPK import ParsedAPK
from selfdroid.appstorage.crud.AppDeleter import AppDeleter
from selfdroid.appstorage.crud.AppUpdaterException import AppUpdaterException
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid import db


class AppUpdater:
    """
    This class must be instantiated and have its public methods called in a locked context!
    """

    def __init__(self, db_model: AppMetadataDBModel, uploaded_apk_path: str):
        self._db_model: AppMetadataDBModel = db_model
        self._app_metadata: AppMetadata =  AppMetadata.from_db_model(db_model)

        self._uploaded_apk_path: str = uploaded_apk_path
        self._parsed_apk: ParsedAPK = APKParser(self._uploaded_apk_path).parsed_apk

    def update_app_while_locked(self) -> Tuple[AppMetadata, AppMetadata]:
        """
        :return: A 2-tuple containing the old (before the update) and new (after the update) app's metadata.
        """

        try:
            updated_app_metadata = self._update_app_while_locked_with_exceptions_handled()

        except UserReadableException as e:
            # User-readable exceptions (AppUpdaterException and APKParserException in this case) cannot cause an
            # "partially updated app", so they can be safely reraised without deleting the app
            raise e

        except Exception as e:
            db.session.rollback()

            # From the AppStorageConsistencyEnsurer class's docstring:
            #  It should be noted that this class does not recognize "partially updated apps" (e.g. apps where the metadata in
            #  the database were updated but the app icon wasn't due to an error).
            #  When an error occurs while updating an app, it should be deleted!
            try:
                AppDeleter(self._db_model).delete_app_while_locked()
            except UserReadableException:
                # An exception is going to be raised anyway, so it's safely possible to ignore this one, if it is raised.
                pass

            if isinstance(e, (sqlalchemy.exc.SQLAlchemyError, OSError)):  # These exceptions can happen, so an alternative user-readable exception is raised
                raise AppUpdaterException("An error occurred while updating the app!")

            raise e  # All other exceptions are unexpected, so they are reraised (which will usually result in a 500 Internal Server Error HTTP response)

        finally:
            AppStorageConsistencyEnsurer().ensure_consistency_while_locked()

        return self._app_metadata, updated_app_metadata

    def _update_app_while_locked_with_exceptions_handled(self) -> AppMetadata:
        self._check_if_app_can_be_updated()

        return self._perform_app_update()

    def _check_if_app_can_be_updated(self) -> None:
        if self._app_metadata.package_name != self._parsed_apk.package_name:
            html_message = WebStatusMessageCollector.format_html_message("The package name of the supplied APK file <i>({})</i> is not the same as the updated app's <i>({})</i>! You should add the app instead of updating it!", self._parsed_apk.package_name, self._app_metadata.package_name)
            raise AppUpdaterException(html_message)

        if self._app_metadata.version_code >= self._parsed_apk.version_code:
            html_message = WebStatusMessageCollector.format_html_message("The version of the supplied APK file <i>({})</i> is not greater than the version of the APK already present on the server <i>({})</i>! Make sure you're uploading a newer version of the app!", self._parsed_apk.version_code, self._app_metadata.version_code)
            raise AppUpdaterException(html_message)

    def _perform_app_update(self) -> AppMetadata:
        # An UserReadableException mustn't be raised in this method!

        # 1. Database
        self._parsed_apk.fill_existing_db_model_with_metadata(self._db_model)
        db.session.commit()

        assert isinstance(self._db_model.id, int)

        updated_app_metadata = AppMetadata.from_db_model(self._db_model)

        # 2. APK
        apk_path = updated_app_metadata.get_apk_path()

        os.remove(apk_path)
        os.rename(self._uploaded_apk_path, apk_path)

        # 3. Icon
        icon_path = updated_app_metadata.get_icon_path()

        os.remove(icon_path)
        with open(icon_path, "wb") as icon_file:
            icon_file.write(self._parsed_apk.uniform_png_app_icon)

        return updated_app_metadata
