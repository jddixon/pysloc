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

cdef class Handle:
    cdef:
        Loop loop
        bint cancelled

        str meth_name
        int cb_type
        void *callback
        object arg1, arg2, arg3, arg4

        object __weakref__

        readonly _source_traceback

    cdef inline _set_loop(self, Loop loop)
    cdef inline _run(self)
    cdef _cancel(self)


cdef class TimerHandle:
    cdef:
        object callback, args
        bint closed
        UVTimer timer
        Loop loop
        object __weakref__

        readonly _source_traceback

    cdef _run(self)
    cdef _cancel(self)
