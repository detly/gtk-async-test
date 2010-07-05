#!/usr/bin/python2.6

"""
Copyright (c) 2010, Jason Heeris
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name "Jason Heeris" nor the names of any contributors may be
      used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL JASON HEERIS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import threading

import gobject
import glib

class MyModel(gobject.GObject):
    
    __gproperties__ = {
        'progress'  :   (gobject.TYPE_FLOAT,
                         "progress of operation",
                         "progress of operation",
                         0.0, 1.0,
                         0.0,
                         gobject.PARAM_READABLE)
    }
    
    __gsignals__ = {
        'operation-started' :   (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 ()),
                                 
        'operation-complete':   (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_NONE,
                                 (gobject.TYPE_INT,))
    }

    def __init__(self):
        self.progress = 0.0
        super(MyModel, self).__init__()
    
    def do_set_properties(self, prop, val):
        raise AttributeError("Cannot set property: %s" % prop.name)

    def do_get_properties(self, prop, val):
        if prop.name == 'progress':
            return self.progress
        
        raise AttributeError("Cannot read property: %s" % prop.name)

    def update_progress(self, newvalue):
        self.progress = min(max(newvalue, 0.0), 1.0)
        self.notify('progress')

    def start_operation(self):
        self.emit('operation-started')
        worker = threading.Thread(
                    target=do_long_processing,
                    args=self.operation_complete)
        worker.start()
        
    def operation_complete(self, result):
        self.emit('operation-complete', result)

gobject.type_register(MyModel)