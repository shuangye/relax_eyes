"""
This program reminds you to relax after working for a certain period.
"""

"""
Copyright © 2020 <Harper Liu, https://github.com/shuangye/relax_eyes>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import webbrowser
from tkinter import *

g_root                          = None
g_workDuration                  = 30 * 60   # in seconds; change as needed
g_relaxDuration                 = 5 * 60    # in seconds; change as needed
g_notifyDurationBeforeRelax     = 20        # in seconds; change as needed
gc_FONT                         = 'Helvetica'
gc_DEFAULT_BG_COLOR             = '#DDDDDD'
gc_DEFAULT_FG_COLOR             = 'black'
gc_NOTIFY_FG_COLOR              = 'orange'
gc_RELAX_FG_COLOR               = gc_DEFAULT_BG_COLOR
gc_RELAX_BG_COLOR               = gc_DEFAULT_FG_COLOR
gc_TIMER_RESOLUTION             = 1         # in seconds
gc_REPO_URL                     = 'https://github.com/shuangye/relax_eyes'
gc_MODE_RELAX                   = 0
gc_MODE_WORK                    = 1

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.lapsed = 0
        self.mode = gc_MODE_WORK
        self.countdownText = StringVar()
        self.pack(expand = True, fill = 'both')
        self.place(in_ = master, anchor = CENTER, relx = .5, rely = .5)
        self.createWidgets()
        self.timeMeas()

    def createWidgets(self):
        self.statusLabel = Label(self, font = (gc_FONT, 60), pady = 20)
        self.statusLabel.pack()
        self.countdownLabel = Label(self, font = (gc_FONT, 200), textvariable = self.countdownText, pady = 30)
        self.countdownLabel.pack()
        self.bottomFrame = Frame(master = self.master)
        self.bottomFrame.pack(expand = True, fill = X, anchor = S, side = BOTTOM)
        self.actionButton = Button(self.bottomFrame, font = (gc_FONT, 20), command = self.relax, borderwidth = 0, padx = 10, pady = 10)
        self.actionButton.pack(side = RIGHT, anchor = SE)
        self.copyLabel = Label(self.bottomFrame, font = (gc_FONT, 10), text = '© 2020 <Harper Liu, {0}>'.format(gc_REPO_URL), cursor="hand2")
        self.copyLabel.pack(side = LEFT, anchor = SW)
        self.copyLabel.bind("<Button-1>", lambda e: webbrowser.open_new(gc_REPO_URL))
        self.configureUI()

    def timeMeas(self):
        self.after(gc_TIMER_RESOLUTION * 1000, self.timeMeas)
        self.lapsed += gc_TIMER_RESOLUTION
        if (self.mode == gc_MODE_RELAX):
            remaining = g_relaxDuration - self.lapsed
            if remaining == 0: self.work()
        else:
            remaining = g_workDuration - self.lapsed
            if remaining == 0: self.relax()
            elif remaining == g_notifyDurationBeforeRelax:
                self.countdownLabel.configure(fg = gc_NOTIFY_FG_COLOR)
                self.bringUpWindow(True)
        self.countdownText.set("{0:02}:{1:02}".format(remaining // 60, remaining % 60))

    def bringUpWindow(self, temporary):
        g_root.update()
        g_root.deiconify()
        # g_root.state('normal')                # may not work on non-Windows OS
        g_root.lift()                           # Thank you https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
        g_root.attributes('-topmost', True)
        if temporary: g_root.attributes('-topmost', False)

    def configureUI(self):
        if self.mode == gc_MODE_RELAX: bgColor = gc_RELAX_BG_COLOR; fgColor = gc_RELAX_FG_COLOR; statusLebel = 'Time To Work';
        else: bgColor = gc_DEFAULT_BG_COLOR; fgColor = gc_DEFAULT_FG_COLOR; statusLebel = 'Time To Relax';
        g_root.configure(bg = bgColor)
        self.configure(bg = bgColor)
        self.bottomFrame.configure(bg = bgColor)
        self.statusLabel.configure(bg = bgColor, fg = fgColor, text = statusLebel)
        self.countdownLabel.configure(bg = bgColor, fg = fgColor)
        self.copyLabel.configure(bg = bgColor, fg = fgColor)
        if self.mode == gc_MODE_RELAX:
            self.actionButton.configure(bg = bgColor, fg = fgColor, text = 'Work Now', command = self.work)
            toggleFullscreen(True)
            self.bringUpWindow(False)
        else:
            self.actionButton.configure(bg = bgColor, fg = fgColor, text = 'Relax Now', command = self.relax)
            toggleFullscreen(False)
            self.bringUpWindow(True)

    def work(self):
        self.mode = gc_MODE_WORK
        self.lapsed = 0
        self.configureUI()

    def relax(self):
        self.mode = gc_MODE_RELAX
        self.lapsed = 0
        self.configureUI()

def toggleFullscreen(full):
    g_root.attributes('-fullscreen', full)

def main():
    global g_root
    g_root = Tk()
    g_root.title('Relax Eyes')
    g_root.resizable(True, True)
    g_root.geometry("{}x{}".format(g_root.winfo_screenwidth() // 2, g_root.winfo_screenheight() // 2))
    # g_root.state('zoomed')  # maximize
    g_root.configure(bg = gc_DEFAULT_BG_COLOR)
    app = Application(master = g_root)
    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) >= 3:  # specify duration in minutes
        g_workDuration = int(sys.argv[1]) * 60
        g_relaxDuration = int(sys.argv[2]) * 60
    main()
