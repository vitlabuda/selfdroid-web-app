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


import os
import threading
import fcntl


class FlockBasedLock:
    """
    FlockBasedLock is a Python 3 library which allows even completely unrelated processes or threads to acquire and then
    release atomic locks bound to a specific file. As the name suggests, it uses the flock() syscall to perform the
    (un)locking.

    The locking may be performed using the "with" statement, or the acquire() and release() methods.

    The library has been written for Linux, but it will probably work on other Unixes as well.
    Tested on Debian 10 (Linux 4.19) with Python 3.7.
    """

    class LockClosedException(Exception):
        """
        This exception is raised when an instance whose file descriptor used for locking has already been closed is
        used for locking or unlocking.
        """

        def __init__(self):
            super().__init__("The lock has been closed!")

    LIBRARY_VERSION: int = 1

    def __init__(self, filepath: str, single_use: bool = False):
        """
        Initializes a new FlockBasedLock instance.

        :param filepath: The path of the file to bind the lock to.
        :param single_use: If True, the lock is automatically closed when it is released.
        """

        self._fd = os.open(filepath, os.O_WRONLY | os.O_TRUNC | os.O_CREAT)
        self._is_open: bool = True
        self._single_use: bool = single_use
        self._threading_lock: threading.Lock = threading.Lock()

    def acquire(self) -> None:
        """Acquire the lock."""

        with self._threading_lock:
            self._acquire()

    def _acquire(self) -> None:
        if not self._is_open:
            raise FlockBasedLock.LockClosedException()

        fcntl.flock(self._fd, fcntl.LOCK_EX)

    def release(self) -> None:
        """Release the previously acquired lock."""

        with self._threading_lock:
            self._release()

    def _release(self) -> None:
        if not self._is_open:
            raise FlockBasedLock.LockClosedException()

        fcntl.flock(self._fd, fcntl.LOCK_UN)

        if self._single_use:
            self._close()

    def close(self) -> None:
        """
        Close the file descriptor used for locking.

        The instance may not be used for locking after it has been closed.
        """

        with self._threading_lock:
            self._close()

    def _close(self) -> None:
        if self._is_open:
            os.close(self._fd)
            self._is_open = False

    def __enter__(self):
        """Acquire the lock."""

        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release the previously acquired lock."""

        self.release()

    def __del__(self):
        try:
            self.close()
        except OSError:
            pass
