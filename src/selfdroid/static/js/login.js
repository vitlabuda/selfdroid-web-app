/*
SPDX-License-Identifier: BSD-3-Clause

Copyright (c) 2021 Vít Labuda. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:
 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.
 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/


function set_up_password_field_hiding_if_needed() {
    function hide_password_field_if_needed_callback() {
        const log_in_as_user_radio_field = document.querySelector('.selfdroid-log-in-as-radio-field[value="user"]');
        const passwordless_login_note = document.querySelector("#passwordless-login-note");
        const password_field_wrapper = document.querySelector("#password-field-wrapper");

        // The IS_USER_LOGIN_PASSWORDLESS constant is declared dynamically using Jinja2 in the base template
        if(IS_USER_LOGIN_PASSWORDLESS && log_in_as_user_radio_field.checked) {
            passwordless_login_note.style.display = "block";
            password_field_wrapper.style.display = "none";
        } else {
            passwordless_login_note.style.display = "none";
            password_field_wrapper.style.display = "block";
        }
    }


    const log_in_as_radio_fields = document.querySelectorAll(".selfdroid-log-in-as-radio-field");
    for(let i = 0; i < log_in_as_radio_fields.length; i++)
        log_in_as_radio_fields[i].addEventListener("change", hide_password_field_if_needed_callback);

    hide_password_field_if_needed_callback();
}

function show_mobile_app_companion_info() {
    const api_url = ("https://" + API_HOST + API_PATH);

    // --- QR code ---
    // QRCode.js documentation: https://github.com/davidshimjs/qrcodejs
    const api_url_qrcode_element = document.querySelector("#api-url-qrcode");
    new QRCode(api_url_qrcode_element, {
        text: api_url,
        width: 256,
        height: 256
    });

    // --- Manual ---
    const api_url_text_element = document.querySelector("#api-url-text");
    api_url_text_element.innerHTML = api_url;
}

window.onload = function() {
    set_up_password_field_hiding_if_needed();

    show_mobile_app_companion_info();
}
