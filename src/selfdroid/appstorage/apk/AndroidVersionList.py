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


from typing import Dict


class AndroidVersionList:
    # API level -> human-readable version string
    _ANDROID_VERSIONS: Dict[int, str] = {
        1: "Android 1.0",
        2: "Android 1.1 (Petit Four)",
        3: "Android 1.5 (Cupcake)",
        4: "Android 1.6 (Donut)",
        5: "Android 2.0 (Eclair)",
        6: "Android 2.0.1 (Eclair)",
        7: "Android 2.1 (Eclair)",
        8: "Android 2.2–2.2.3 (Froyo)",
        9: "Android 2.3–2.3.2 (Gingerbread)",
        10: "Android 2.3.3–2.3.7 (Gingerbread)",
        11: "Android 3.0 (Honeycomb)",
        12: "Android 3.1 (Honeycomb)",
        13: "Android 3.2–3.2.6 (Honeycomb)",
        14: "Android 4.0–4.0.2 (Ice Cream Sandwich)",
        15: "Android 4.0.3–4.0.4 (Ice Cream Sandwich)",
        16: "Android 4.1–4.1.2 (Jelly Bean)",
        17: "Android 4.2–4.2.2 (Jelly Bean)",
        18: "Android 4.3–4.3.1 (Jelly Bean)",
        19: "Android 4.4–4.4.4 (KitKat)",
        20: "Android 4.4W–4.4W.2 (KitKat)",
        21: "Android 5.0–5.0.2 (Lollipop)",
        22: "Android 5.1–5.1.1 (Lollipop)",
        23: "Android 6.0–6.0.1 (Marshmallow)",
        24: "Android 7.0 (Nougat)",
        25: "Android 7.1–7.1.2 (Nougat)",
        26: "Android 8.0 (Oreo)",
        27: "Android 8.1 (Oreo)",
        28: "Android 9 (Pie)",
        29: "Android 10",
        30: "Android 11",
        31: "Android 12"
    }

    _UNKNOWN_ANDROID_VERSION: str = "Unknown Android version (API level {})"

    @classmethod
    def get_human_readable_android_version_string_by_api_level(cls, api_version_number: int) -> str:
        if api_version_number in cls._ANDROID_VERSIONS:
            return cls._ANDROID_VERSIONS[api_version_number]

        return cls._UNKNOWN_ANDROID_VERSION.format(api_version_number)
