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


from typing import Dict, Any
import os
import os.path
from selfdroid.EndpointWithAppIDBase import EndpointWithAppIDBase
from selfdroid.UserReadableException import UserReadableException
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.crud.AppGetter import AppGetter
from selfdroid.appstorage.crud.AppUpdater import AppUpdater
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid.web.endpointbases.WebAdminEndpointBase import WebAdminEndpointBase
from selfdroid.web.forms.WebUpdateAppForm import WebUpdateAppForm


class WebUpdateAppEndpoint(WebAdminEndpointBase, EndpointWithAppIDBase):
    def __init__(self, url_params: Dict[str, Any]):
        WebAdminEndpointBase.__init__(self, url_params)
        EndpointWithAppIDBase.__init__(self, url_params)

        self._app_getter: AppGetter = AppGetter()

    def handle_request(self) -> None:
        update_app_form = WebUpdateAppForm()
        self.message_collector.register_form("update_app", update_app_form)

        if update_app_form.validate_on_submit():
            should_request_be_redirected_to_app_details_page = self._lock_and_perform_app_update(update_app_form)
            if should_request_be_redirected_to_app_details_page:
                self.redirect_and_finish_request("web_blueprint.fl_web_app_details", app_id=self.app_id_from_url_params)

        self.redirect_and_finish_request("web_blueprint.fl_web_index")

    def _lock_and_perform_app_update(self, update_app_form: WebUpdateAppForm) -> bool:
        """
        :return: Whether the request should be redirected to the app details page.
        """

        with AppStorageHelpers.get_app_storage_lock():
            self._perform_app_update_while_locked(update_app_form)

            # The check needs to be performed in this fairly unexpected place due to the locked context requirement.
            return self._should_request_be_redirected_to_app_details_page_while_locked()

    def _perform_app_update_while_locked(self, update_app_form: WebUpdateAppForm) -> None:
        db_model = self._app_getter.get_db_model_or_404_while_locked(self.app_id_from_url_params)
        apk_file = update_app_form.apk_file.data

        temporary_filepath = AppStorageHelpers.generate_temp_filepath_for_apk_while_locked()
        try:
            apk_file.save(temporary_filepath)
            old_app_metadata, new_app_metadata = AppUpdater(db_model, temporary_filepath).update_app_while_locked()

        except UserReadableException as e:  # AppStorageModificationException and its children, APKParserException
            self.message_collector.add_error_message_from_user_readable_exception(e)

        else:
            if old_app_metadata.app_name == new_app_metadata.app_name:
                html_message = WebStatusMessageCollector.format_html_message("The app <b>{}</b> was successfully updated!", new_app_metadata.app_name)
            else:
                html_message = WebStatusMessageCollector.format_html_message("The app <b>{}</b> (previously named <b>{}</b>) was successfully updated!", new_app_metadata.app_name, old_app_metadata.app_name)

            self.message_collector.add_success_message(html_message)

        finally:
            if os.path.exists(temporary_filepath):
                os.remove(temporary_filepath)

    def _should_request_be_redirected_to_app_details_page_while_locked(self) -> bool:
        # The decision whether to redirect the request or not is not based on the update operation's result,
        # because even if the app failed to update, it is, in most cases (unless it was deleted due to a fatal error),
        # still present in the app storage.

        return self._app_getter.does_app_exist_in_database(self.app_id_from_url_params)
