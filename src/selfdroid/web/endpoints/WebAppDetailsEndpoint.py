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
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.crud.AppGetter import AppGetter
from selfdroid.web.endpointbases.WebAtLeastUserEndpointBase import WebAtLeastUserEndpointBase
from selfdroid.web.forms.WebUpdateAppForm import WebUpdateAppForm
from selfdroid.web.forms.WebDeleteAppForm import WebDeleteAppForm


class WebAppDetailsEndpoint(WebAtLeastUserEndpointBase, EndpointWithAppIDBase):
    def __init__(self, url_params: Dict[str, Any]):
        WebAtLeastUserEndpointBase.__init__(self, url_params)
        EndpointWithAppIDBase.__init__(self, url_params)

    def handle_request(self) -> None:
        with AppStorageHelpers.get_app_storage_lock():
            app_metadata = AppGetter().get_metadata_or_404_while_locked(self.app_id_from_url_params)

        template_context = {"app_metadata": app_metadata}
        if self.authenticator.has_admin_privileges():
            template_context["update_app_form"] = WebUpdateAppForm()
            template_context["delete_app_form"] = WebDeleteAppForm()

        self.render_template_and_finish_request("web_app_details.html", **template_context)
