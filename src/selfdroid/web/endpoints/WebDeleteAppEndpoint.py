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
from selfdroid.EndpointWithAppIDBase import EndpointWithAppIDBase
from selfdroid.UserReadableException import UserReadableException
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.crud.AppGetter import AppGetter
from selfdroid.appstorage.crud.AppDeleter import AppDeleter
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid.web.endpointbases.WebAdminEndpointBase import WebAdminEndpointBase
from selfdroid.web.forms.WebDeleteAppForm import WebDeleteAppForm


class WebDeleteAppEndpoint(WebAdminEndpointBase, EndpointWithAppIDBase):
    def __init__(self, url_params: Dict[str, Any]):
        WebAdminEndpointBase.__init__(self, url_params)
        EndpointWithAppIDBase.__init__(self, url_params)

        self._app_getter: AppGetter = AppGetter()

    def handle_request(self) -> None:
        delete_app_form = WebDeleteAppForm()
        self.message_collector.register_form("delete_app", delete_app_form)

        if delete_app_form.validate_on_submit():
            self._lock_and_perform_app_deletion()
            # The likelihood of the deletion failing is so small that it would be a waste of time to add a redirection
            # to the app's details page there

        self.redirect_and_finish_request("web_blueprint.fl_web_index")

    def _lock_and_perform_app_deletion(self) -> None:
        with AppStorageHelpers.get_app_storage_lock():
            self._perform_app_deletion_while_locked()

    def _perform_app_deletion_while_locked(self) -> None:
        db_model = self._app_getter.get_db_model_or_404_while_locked(self.app_id_from_url_params)

        try:
            app_metadata = AppDeleter(db_model).delete_app_while_locked()

        except UserReadableException as e:
            self.message_collector.add_error_message_from_user_readable_exception(e)

        else:
            html_message = WebStatusMessageCollector.format_html_message("The app <b>{}</b> was successfully deleted!", app_metadata.app_name)
            self.message_collector.add_success_message(html_message)
