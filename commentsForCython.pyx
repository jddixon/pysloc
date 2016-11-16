# The MIT License
# 
# Copyright (c) 2015-present MagicStack Inc.  http://magic.io
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

cdef class Server:
    def __cinit__(self, Loop loop):
        self._loop = loop
        self._servers = []
        self._waiters = []
        self._active_count = 0

    cdef _add_server(self, UVStreamServer srv):
        self._servers.append(srv)

    cdef _wakeup(self):
        cdef list waiters

        waiters = self._waiters
        self._waiters = None
        for waiter in waiters:
            if not waiter.done():
                waiter.set_result(waiter)

    cdef _attach(self):
        assert self._servers is not None
        self._active_count += 1

    cdef _detach(self):
        assert self._active_count > 0
        self._active_count -= 1
        if self._active_count == 0 and self._servers is None:
            self._wakeup()

    # Public API

    def __repr__(self):
        return '<%s sockets=%r>' % (self.__class__.__name__, self.sockets)

    async def wait_closed(self):
        if self._servers is None or self._waiters is None:
            return
        waiter = self._loop._new_future()
        self._waiters.append(waiter)
        await waiter

    def close(self):
        if self._servers is None:
            return

        cdef list servers = self._servers
        self._servers = None

        for server in servers:
            (<UVStreamServer>server)._close()

        if self._active_count == 0:
            self._wakeup()

    property sockets:
        def __get__(self):
            cdef list sockets = []

            for server in self._servers:
                sockets.append(
                    (<UVStreamServer>server)._get_socket()
                )

            return sockets
