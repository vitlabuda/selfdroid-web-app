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


from typing import Set
import os
import re
import sqlalchemy.exc
from selfdroid.Constants import Constants
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel
from selfdroid import db


class AppStorageConsistencyEnsurer:
    """
    The purpose of this class is described in the NOTES file.

    It should be noted that this class does not recognize "partially updated apps" (e.g. apps where the metadata in
    the database were updated but the app icon wasn't due to an error).
    When an error occurs while updating an app, it should be deleted!
    """

    class _NoSuchDBEntryException(Exception):
        # For this class's internal use
        pass

    def ensure_consistency_while_locked(self) -> None:
        db_app_ids = self._get_all_app_ids_from_database()
        apks_directory_app_ids = self._get_all_app_ids_from_a_directory(Constants.APKS_DIRECTORY, "apk")
        icons_directory_app_ids = self._get_all_app_ids_from_a_directory(Constants.ICONS_DIRECTORY, "png")

        # This variable contains app IDs that aren't present in all of these 3 sets (= apps that aren't present in all of the app storage places).
        # Such apps are considered inconsistent and thus deleted.
        inconsistent_app_ids = (db_app_ids | apks_directory_app_ids | icons_directory_app_ids) - (db_app_ids & apks_directory_app_ids & icons_directory_app_ids)

        for app_id in inconsistent_app_ids:
            self._delete_app_from_all_places(app_id)

    def _delete_app_from_all_places(self, app_id: int) -> None:
        try:
            db_entry = AppMetadataDBModel.query.get(app_id)
            if not db_entry:
                raise AppStorageConsistencyEnsurer._NoSuchDBEntryException()

            db.session.delete(db_entry)
            db.session.commit()

        except (sqlalchemy.exc.SQLAlchemyError, AppStorageConsistencyEnsurer._NoSuchDBEntryException):
            db.session.rollback()

        apk_path = AppStorageHelpers.get_apk_path_by_app_id(app_id)
        try:
            os.remove(apk_path)
        except OSError:
            pass

        icon_path = AppStorageHelpers.get_icon_path_by_app_id(app_id)
        try:
            os.remove(icon_path)
        except OSError:
            pass

    def _get_all_app_ids_from_database(self) -> Set[int]:
        db_entries = AppMetadataDBModel.query.all()
        app_ids_iter = map(lambda db_entry: db_entry.id, db_entries)

        return set(app_ids_iter)

    def _get_all_app_ids_from_a_directory(self, directory_path: str, filename_extension: str) -> Set[int]:
        regex = r'^\d+\.{}$'.format(filename_extension)
        slice_stop = -(len(filename_extension) + 1)  # Cuts the filename extension and the dot before it -> only the app ID (integer) gets extracted from the filename

        directory_listing = os.listdir(directory_path)
        matching_filenames_iter = filter(lambda directory_item: re.match(regex, directory_item), directory_listing)
        app_ids_iter = map(lambda matching_filename: int(matching_filename[:slice_stop]), matching_filenames_iter)

        return set(app_ids_iter)
