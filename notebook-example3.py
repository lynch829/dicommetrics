import wx


# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.

class ResultsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Add the ListCtrl widget to the results panel. The ListCtrl widget
        # displays the list of metrics with their results.
        ListBox = wx.ListCtrl(self, -1, size=(728,728), style=wx.LC_REPORT|wx.LC_HRULES)

        # Add the column headers to the list of metrics.
        ListBox.InsertColumn(0, 'Name')
        ListBox.InsertColumn(1, 'Result')
        ListBox.InsertColumn(2, 'Score')
        ListBox.InsertColumn(3, 'Max Score')
        ListBox.InsertColumn(4, 'Rel Score')

class AlgPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Add a big text box to the algorithm panel. The text box widget
        # displays the currently loaded algorithm. In the future, it will also
        # allow editing the algorithm and updating the results.
        AlgBox = wx.TextCtrl(self, -1, size=(728,728), 
                             style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_DONTWRAP)


        AlgFont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        AlgBox.SetFont(AlgFont)



class DVHPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        DummyText = wx.StaticText(self, -1, 
                                  'This is will display the DVH of the current patient.', 
                                  size=(728,400), style=wx.ALIGN_CENTRE_HORIZONTAL)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simple Notebook Example", size=(1024,728))

        # Here we create a panel and a notebook on the panel
        MainPanel = wx.Panel(self)
        NoteView = wx.Notebook(MainPanel, style=wx.NB_TOP)

        # create the page windows as children of the notebook
        page1 = ResultsPanel(NoteView)
        page2 = AlgPanel(NoteView)
        page3 = DVHPanel(NoteView)

        # add the pages to the notebook with the label to show on the tab
        NoteView.AddPage(page1, "Results")
        NoteView.AddPage(page2, "Algorithm")
        NoteView.AddPage(page3, "DVH")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        MainSizer = wx.BoxSizer()
        MainSizer.Add(NoteView, 1, wx.EXPAND)
        MainPanel.SetSizer(MainSizer)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
