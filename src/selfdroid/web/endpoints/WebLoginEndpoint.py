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


from selfdroid.UserReadableException import UserReadableException
from selfdroid.web.endpointbases.WebPublicOnlyEndpointBase import WebPublicOnlyEndpointBase
from selfdroid.web.forms.WebLoginForm import WebLoginForm


class WebLoginEndpoint(WebPublicOnlyEndpointBase):
    def handle_request(self) -> None:
        login_form = WebLoginForm()
        self.message_collector.register_form("login", login_form)

        is_user_login_passwordless = self.authenticator.is_user_login_passwordless()

        if login_form.validate_on_submit():
            self._perform_login(login_form)
            self.redirect_and_finish_request("web_blueprint.fl_web_index")

        self.render_template_and_finish_request("web_login.html", login_form=login_form, is_user_login_passwordless=is_user_login_passwordless)

    def _perform_login(self, login_form: WebLoginForm) -> None:
        password = login_form.password.data

        try:
            if login_form.log_in_as.data == "admin":
                self.authenticator.log_in_as_admin(password)
            else:
                self.authenticator.log_in_as_user(password)

        except UserReadableException as e:  # WebAuthenticatorLoginException
            self.message_collector.add_error_message_from_user_readable_exception(e)
