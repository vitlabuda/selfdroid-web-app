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
import os
import os.path
from selfdroid.UserReadableException import UserReadableException
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.AppMetadata import AppMetadata
from selfdroid.appstorage.crud.AppAdder import AppAdder
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid.web.endpointbases.WebAdminEndpointBase import WebAdminEndpointBase
from selfdroid.web.forms.WebAddAppForm import WebAddAppForm


class WebAddAppEndpoint(WebAdminEndpointBase):
    def handle_request(self) -> None:
        add_app_form = WebAddAppForm()
        self.message_collector.register_form("add_app", add_app_form)

        if add_app_form.validate_on_submit():
            app_metadata = self._lock_and_perform_app_addition(add_app_form)
            if app_metadata is not None:  # = If the app was successfully added to the database
                self.redirect_and_finish_request("web_blueprint.fl_web_app_details", app_id=app_metadata.id)

        self.redirect_and_finish_request("web_blueprint.fl_web_index")

    def _lock_and_perform_app_addition(self, add_app_form: WebAddAppForm) -> Optional[AppMetadata]:
        with AppStorageHelpers.get_app_storage_lock():
            return self._perform_app_addition_while_locked(add_app_form)

    def _perform_app_addition_while_locked(self, add_app_form: WebAddAppForm) -> Optional[AppMetadata]:
        apk_file = add_app_form.apk_file.data

        temporary_filepath = AppStorageHelpers.generate_temp_filepath_for_apk_while_locked()
        try:
            apk_file.save(temporary_filepath)
            app_metadata = AppAdder(temporary_filepath).add_app_while_locked()

        except UserReadableException as e:  # AppStorageModificationException and its children, APKParserException
            self.message_collector.add_error_message_from_user_readable_exception(e)

            return None

        else:
            html_message = WebStatusMessageCollector.format_html_message("The app <b>{}</b> was successfully added!", app_metadata.app_name)
            self.message_collector.add_success_message(html_message)

            return app_metadata

        finally:
            if os.path.exists(temporary_filepath):  # The file might have been moved
                os.remove(temporary_filepath)
