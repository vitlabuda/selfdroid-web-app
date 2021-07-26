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
import abc
import flask
from selfdroid.EndpointBase import EndpointBase
from selfdroid.web.WebStatusMessageCollector import WebStatusMessageCollector
from selfdroid.web.authenticator.WebAuthenticator import WebAuthenticator


class WebEndpointBase(EndpointBase, metaclass=abc.ABCMeta):
    def __init__(self, url_params: Dict[str, Any]):
        super().__init__(url_params)

        self.authenticator: WebAuthenticator = WebAuthenticator()
        self.message_collector: WebStatusMessageCollector = WebStatusMessageCollector()

        requires_authentication = self._requires_authentication()
        is_client_authenticated = self._is_client_authenticated()

        if requires_authentication and not is_client_authenticated:
            self.redirect_and_finish_request("web_blueprint.fl_web_login")
        elif not requires_authentication and is_client_authenticated:
            self.redirect_and_finish_request("web_blueprint.fl_web_index")

    @abc.abstractmethod
    def _requires_authentication(self) -> bool:
        raise NotImplementedError("The _requires_authentication() method must be overridden prior to calling it!")

    @abc.abstractmethod
    def _is_client_authenticated(self) -> bool:
        raise NotImplementedError("The _is_client_authenticated() method must be overridden prior to calling it!")

    def redirect_and_finish_request(self, endpoint_name: str, **url_params) -> None:
        self.message_collector.flash_all_messages_using_flask()

        redirect = flask.redirect(flask.url_for(endpoint_name, **url_params))
        self.finish_request(redirect)

    def render_template_and_finish_request(self, template_name: str, **params) -> None:
        params["status_messages"] = self.message_collector.get_all_messages_including_flask_flashed_messages()

        rendered_template = flask.render_template(template_name, **params)
        self.finish_request(rendered_template)

    def send_file_and_finish_request(self, directory: str, filename: str, download_name: str, **send_file_kwargs) -> None:
        send_file_kwargs["download_name"] = download_name

        sent_file = flask.send_from_directory(directory, filename, **send_file_kwargs)
        self.finish_request(sent_file)
