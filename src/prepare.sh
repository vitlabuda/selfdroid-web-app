#!/bin/bash

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


function exit_with_error() {
  echo "ERROR: $1"
  echo 'Delete the "virtualenv" and "self_signed_certs" directories if they exist any try again!'
  exit 1
}


# Traverse to the directory where this script is located
cd -- "$(dirname -- "$0")" || exit_with_error "Failed to traverse into the script's directory"

# Generate a new self-signed certificate
if [ ! -d "./self_signed_certs" ]; then
  mkdir './self_signed_certs' || exit_with_error "Failed to create a new directory for the self-signed certificate"
  chmod 0700 './self_signed_certs' || exit_with_error "Failed to change the self-signed certificates directory's permissions"

  openssl req \
    -x509 \
    -newkey rsa:4096 \
    -keyout './self_signed_certs/private_key.key' \
    -out './self_signed_certs/certificate.crt' \
    -days 1825 \
    -nodes \
    -subj '/O=Selfdroid/OU=Self-Signed Certificate - DO NOT TRUST!/CN=localhost' || exit_with_error "Failed to generate a new self-signed certificate"

  chmod 0600 './self_signed_certs/private_key.key' './self_signed_certs/certificate.crt' || exit_with_error "Failed to change the certificate's and private key's permissions"
fi

# Prepare a virtual environment
if [ ! -d "./virtualenv" ]; then
  virtualenv -p python3 virtualenv || exit_with_error "Failed to create Python virtual environment"
  . ./virtualenv/bin/activate || exit_with_error "Failed to activate Python virtual environment"
  ./virtualenv/bin/pip3 install -r requirements.txt || exit_with_error "Failed to install the required Python libraries"
fi

# If everything went well, exit with a successful exit code
exit 0
