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
from selfdroid.appstorage.crud.AppDeleterException import AppDeleterException
from selfdroid import db


class AppDeleter:
    """
    This class must be instantiated and have its public methods called in a locked context!
    """

    def __init__(self, db_model: AppMetadataDBModel):
        self._db_model: AppMetadataDBModel = db_model
        self._app_metadata: AppMetadata = AppMetadata.from_db_model(db_model)

    def delete_app_while_locked(self) -> AppMetadata:
        """
        :return: The metadata of the deleted app.
        """

        try:
            self._delete_app_while_locked_with_exceptions_handled()

        except (sqlalchemy.exc.SQLAlchemyError, OSError):
            db.session.rollback()

            raise AppDeleterException("An error occurred while deleting the app!")

        finally:
            AppStorageConsistencyEnsurer().ensure_consistency_while_locked()

        return self._app_metadata

    def _delete_app_while_locked_with_exceptions_handled(self) -> None:
        # No checking needs to be done --> for now, this is just wrapper method for future expansion.

        self._perform_app_deletion()

    def _perform_app_deletion(self) -> None:
        # An UserReadableException mustn't be raised in this method!

        # 1. Database
        db.session.delete(self._db_model)
        db.session.commit()

        # 2. APK
        apk_path = self._app_metadata.get_apk_path()
        os.remove(apk_path)

        # 3. Icon
        icon_path = self._app_metadata.get_icon_path()
        os.remove(icon_path)
