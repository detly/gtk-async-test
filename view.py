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

import gtk

class MyView(gtk.VBox):

    def __init__(self):
        super(MyView, self).__init__()
        self.set_property('spacing', 5)
        self.set_property('homogeneous', False)

        self.progressbar = gtk.ProgressBar()
        self.startbutton = gtk.Button("Start")

        resultdec = gtk.Label("<b>Result:</b>")
        resultdec.set_use_markup(True)

        self.resultlabel = gtk.Label()

        resultbox = gtk.HBox()
        resultbox.set_property('spacing', 5)
        resultbox.pack_start(resultdec, expand=False)
        resultbox.pack_start(self.resultlabel)

        self.pack_start(self.startbutton, expand=False)
        self.pack_start(self.progressbar, expand=False)
        self.pack_start(resultbox, expand=False)

    def on_operation_started(self, source):
        self.startbutton.set_property('sensitive', False)
        self.progressbar.set_fraction(0.0)
        self.resultlabel.set_text("Waiting...")

    def on_operation_complete(self, source, result):
        self.startbutton.set_property('sensitive', True)
        self.resultlabel.set_text(str(result))

    def on_progress_notify(self, source, property):
        # If this was a signal, the property could just be sent as an extra
        # parameter.
        self.progressbar.set_fraction(source.get_property(property.name))

def destroy(widget, data=None):
    gtk.main_quit()

def LaunchUI(view):
    window = gtk.Window()
    window.add(view)

    window.connect('destroy', destroy)

    window.set_title("GTK async test")

    window.show_all()
    gtk.main()
