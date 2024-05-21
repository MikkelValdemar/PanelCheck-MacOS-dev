#!/usr/bin/env python

import wx

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as html
else:
    import wx.html as html


class AboutFrame(wx.Frame):
    def __init__(self, parent):
        """
        The AboutFrame class creates window with information about PanelCheck and
        credits.
        """
        wx.Frame.__init__(self, parent, -1, "About", (-1, -1),
                          (-1, -1), style=wx.MINIMIZE_BOX | wx.CLOSE_BOX)

        if wx.Platform == '__WXMSW__':
            self.html = html.IEHtmlWindow(
                self, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
            self.html.LoadUrl("./resources/about.html")
        else:
            self.html = html.HtmlWindow(
                id=wx.NewId(),
                name='html', parent=self, pos=(-1, -1),
                size=(600, 500),
                style=wx.html.HW_SCROLLBAR_AUTO)
            self.html.LoadPage("./resources/about.html")

        self.button_panel = wx.Panel(self, id=wx.NewId())

        self.icon = wx.Icon("./resources/fig.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html, 1, wx.GROW)

        self.SetSizer(sizer)
        self.SetSize((700, 666))
        self.Layout()

    def closeFrame(self, event):
        """
        Exits the program.

        @type event:    object
        @param event:    An event is a structure holding information about an
        event passed to a callback or member function.
        """
        self.Close()

    def OnLeftDown(self, evt):
        self.Close()


class Starter(wx.App):
    def OnInit(self):
        """
        Creates an AboutFrame class wxFrame and shows it.
        This class makes About.py able to run as independent program.
        """
        frame = AboutFrame(None)
        self.SetTopWindow(frame)
        frame.Show()
        return 1


if __name__ == "__main__":
    import gettext
    gettext.install("app")  # replace with the appropriate catalog name

    app = Starter(0)
    app.MainLoop()
