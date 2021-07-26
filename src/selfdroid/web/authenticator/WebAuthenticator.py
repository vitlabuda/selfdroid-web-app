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


import flask
from selfdroid.Settings import Settings
from selfdroid.Helpers import Helpers
from selfdroid.AuthenticatorBase import AuthenticatorBase
from selfdroid.web.authenticator.WebAuthenticatorLoginException import WebAuthenticatorLoginException
from selfdroid.web.authenticator.WebAuthenticatorLogoutException import WebAuthenticatorLogoutException


class WebAuthenticator(AuthenticatorBase):
    _SESSION_KEY_HAS_USER_PRIVILEGES: str = "web_has_user_privileges"
    _SESSION_KEY_HAS_ADMIN_PRIVILEGES: str = "web_has_admin_privileges"
    _SESSION_KEY_LOGIN_TIMESTAMP: str = "web_login_timestamp"

    def has_at_least_user_privileges(self) -> bool:
        has_user_privileges = flask.session.get(WebAuthenticator._SESSION_KEY_HAS_USER_PRIVILEGES, default=False)
        if not has_user_privileges:
            return False

        login_timestamp = flask.session.get(WebAuthenticator._SESSION_KEY_LOGIN_TIMESTAMP, default=None)
        if login_timestamp is None:
            return False

        if login_timestamp < Settings.MINIMUM_WEB_LOGIN_TIMESTAMP:
            return False

        login_duration = (Helpers.get_current_unix_timestamp() - login_timestamp)
        if login_duration < 0:  # This can only be true if the server's time is changed into the past which shouldn't normally happen
            return False

        if login_duration > Settings.WEB_LOGIN_LIFETIME:
            return False

        return True

    def has_admin_privileges(self) -> bool:
        if not self.has_at_least_user_privileges():
            return False

        has_admin_privileges = flask.session.get(WebAuthenticator._SESSION_KEY_HAS_ADMIN_PRIVILEGES, default=False)
        return has_admin_privileges

    def log_in_as_user(self, password: str) -> None:
        if self.has_at_least_user_privileges():
            raise WebAuthenticatorLoginException("You're already logged in!")

        if self.check_user_password(password):
            self._add_session_variables_on_login(has_admin_privileges=False)
        else:
            raise WebAuthenticatorLoginException("The user password is incorrect! Please try again!")

    def log_in_as_admin(self, password: str) -> None:
        if self.has_at_least_user_privileges():
            raise WebAuthenticatorLoginException("You're already logged in!")

        if self.check_admin_password(password):
            self._add_session_variables_on_login(has_admin_privileges=True)
        else:
            raise WebAuthenticatorLoginException("The administrator password is incorrect! Please try again!")

    def _add_session_variables_on_login(self, has_admin_privileges: bool) -> None:
        flask.session[WebAuthenticator._SESSION_KEY_HAS_USER_PRIVILEGES] = True
        flask.session[WebAuthenticator._SESSION_KEY_HAS_ADMIN_PRIVILEGES] = has_admin_privileges
        flask.session[WebAuthenticator._SESSION_KEY_LOGIN_TIMESTAMP] = Helpers.get_current_unix_timestamp()

    def log_out(self) -> None:
        if not self.has_at_least_user_privileges():
            raise WebAuthenticatorLogoutException("You're not logged in!")

        flask.session.pop(WebAuthenticator._SESSION_KEY_HAS_USER_PRIVILEGES, default=None)
        flask.session.pop(WebAuthenticator._SESSION_KEY_HAS_ADMIN_PRIVILEGES, default=None)
        flask.session.pop(WebAuthenticator._SESSION_KEY_LOGIN_TIMESTAMP, default=None)
