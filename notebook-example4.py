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
        # Initialize the main frame (aka window).
        # Title the window 'DICOM Metrics'.
        # Set the initial size to 1024x768.
        wx.Frame.__init__(self, None, title="Simple Notebook Example", size=(1024,728))

        # Set the dicom listener to be paused on startup of the application.
        self.paused = True

        #
        # Collection of GUI element IDs.
        #
        ID_FILE_OPEN_PATIENT_PLAN     = 201
        ID_FILE_OPEN_PATIENT_RESULTS  = 202
        ID_FILE_SAVE_PATIENT_RESULTS  = 203
        ID_FILE_QUIT      = 204
        ID_CONFIG_LOAD    = 301
        ID_CONFIG_SAVE    = 302
        ID_TOOLBAR_TOGGLE = 303
        ID_HELP_CONTENTS  = 401
        ID_HELP_ABOUT     = 402

        ID_TOOL_OPEN_PATIENT_PLAN     = 10
        ID_TOOL_OPEN_PATIENT_RESULTS  = 20
        ID_TOOL_SAVE_PATIENT_RESULTS  = 30
        ID_TOOL_START = 40
        ID_TOOL_STOP  = 50
        ID_TOOL_QUIT  = 60

        ID_SPLITTER       = 70
        ID_SAVE_MESSAGES  = 80

        #
        # Collection of GUI BMPs.
        #
        # Make image objects for each of the icons on the toolbar:
        # save, start, stop, exit.
        #save_bmp = wx.Image('SaveTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #start_bmp = wx.Image('StartTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #stop_bmp  = wx.Image('StopTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #exit_bmp  = wx.Image('QuitTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        OpenPatientPlanMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (16,16))
        OpenPatientResultsMenuBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16))
        SavePatientResultsMenuBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16,16))
        QuitMenuBMP           = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16,16))
        LoadConfigsMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, (16,16))
        SaveConfigsMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, (16,16))
        HelpContentsMenuBMP   = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_OTHER, (16,16))
        HelpAboutMenuBMP      = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16,16))
        
        OpenPatientPlanToolBMP    = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (32,32))
        OpenPatientResultsToolBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (32,32))
        SavePatientResultsToolBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (32,32))
        #StartToolBMP  = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_OTHER, (32,32))
        #StopToolBMP   = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_OTHER, (32,32))
        StartToolBMP  = wx.Image('StartTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        StopToolBMP   = wx.Image('StopTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        QuitToolBMP   = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (32,32))

        # Here we create a panel and a notebook on the panel
        MainPanel = wx.Panel(self)

        # Make a sizer to hold the info box and notebook widget.
        self.MainArea = wx.BoxSizer(wx.VERTICAL)

        # Initialize a boded box to hold information to be displayed.
        InfoBox = wx.StaticBox(MainPanel, label='')

        # Place a sizer in the info box to hold/arrange the info put in it.
        InfoSizer = wx.FlexGridSizer(rows=3, cols=4)

        # Create static text labels to hold info to be displayed.
        Label11 = wx.StaticText(InfoBox, -1, 'key:')
        Label12 = wx.StaticText(InfoBox, -1, 'value')
        Label13 = wx.StaticText(InfoBox, -1, 'key:')
        Label14 = wx.StaticText(InfoBox, -1, 'value')
        Label21 = wx.StaticText(InfoBox, -1, 'key:')
        Label22 = wx.StaticText(InfoBox, -1, 'value')
        Label23 = wx.StaticText(InfoBox, -1, 'key:')
        Label24 = wx.StaticText(InfoBox, -1, 'value')
        Label31 = wx.StaticText(InfoBox, -1, 'key:')
        Label32 = wx.StaticText(InfoBox, -1, 'value')
        Label33 = wx.StaticText(InfoBox, -1, 'key:')
        Label34 = wx.StaticText(InfoBox, -1, 'value')

        # Add the static text labels to the flex grid sizer.
        InfoSizer.Add(Label11, 0, 0)
        InfoSizer.Add(Label12, 0, 0)
        InfoSizer.Add(Label13, 0, 0)
        InfoSizer.Add(Label14, 0, 0)
        InfoSizer.Add(Label21, 0, 0)
        InfoSizer.Add(Label22, 0, 0)
        InfoSizer.Add(Label23, 0, 0)
        InfoSizer.Add(Label24, 0, 0)
        InfoSizer.Add(Label31, 0, 0)
        InfoSizer.Add(Label32, 0, 0)
        InfoSizer.Add(Label33, 0, 0)
        InfoSizer.Add(Label34, 0, 0)

        # Initialize a notebook view to switch between the results view, algo-
        # oritm view, and DVH view.
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

        # Create the file menu object and give it its menu items.
        filemenu = wx.Menu()
        FileOpenPatientPlan    = wx.MenuItem(filemenu, ID_FILE_OPEN_PATIENT_PLAN, 'Open Patient &Plan...\tCtrl+P')
        FileOpenPatientResults = wx.MenuItem(filemenu, ID_FILE_OPEN_PATIENT_RESULTS, 'Open Patient &Results\tCtrl+R')
        FileSavePatientResults = wx.MenuItem(filemenu, ID_FILE_SAVE_PATIENT_RESULTS, '&Save Patient Results\tCtrl+S')
        FileQuit               = wx.MenuItem(filemenu, ID_FILE_QUIT, '&Quit\tCtrl+Q')

        FileOpenPatientPlan.SetBitmap(OpenPatientPlanMenuBMP)
        FileOpenPatientPlan.SetBitmap(OpenPatientResultsMenuBMP)
        FileSavePatientResults.SetBitmap(SavePatientResultsMenuBMP)
        FileQuit.SetBitmap(QuitMenuBMP)

        filemenu.AppendItem(FileOpenPatientPlan)
        filemenu.AppendItem(FileOpenPatientResults)
        filemenu.AppendItem(FileSavePatientResults)
        filemenu.AppendSeparator()
        filemenu.AppendItem(FileQuit)

        # Create the config menu object and give it its menu items.
        configmenu = wx.Menu()
        LoadConfigs = wx.MenuItem(configmenu, ID_CONFIG_LOAD, '&Load Configuration')
        SaveConfigs = wx.MenuItem(configmenu, ID_CONFIG_SAVE, '&Save Configuration')
        
        LoadConfigs.SetBitmap(LoadConfigsMenuBMP)
        SaveConfigs.SetBitmap(SaveConfigsMenuBMP)
        
        configmenu.AppendItem(LoadConfigs)
        configmenu.AppendItem(SaveConfigs)
        configmenu.AppendSeparator()
        ToolbarToggle = configmenu.Append(ID_TOOLBAR_TOGGLE, 
                                          'Show Toolbar',
                                          'Toggle showing/hiding the toolbar', 
                                          kind=wx.ITEM_CHECK)
        configmenu.Check(ToolbarToggle.GetId(), True)

        # Create the help menu object and give it its menu items.
        helpmenu = wx.Menu()
        HelpContents = wx.MenuItem(helpmenu, ID_HELP_CONTENTS, '&Contents\tF1')
        HelpAbout    = wx.MenuItem(helpmenu, ID_HELP_ABOUT, '&About\tCtrl+A')

        HelpContents.SetBitmap(HelpContentsMenuBMP)
        HelpAbout.SetBitmap(HelpAboutMenuBMP)

        helpmenu.AppendItem(HelpContents)
        helpmenu.AppendItem(HelpAbout)

        # Create the menubar object and give it the above created menu objects.
        # There is only File, Config, and Help as available menus so far.
        MenuBar = wx.MenuBar()
        MenuBar.Append(filemenu,"&File")
        MenuBar.Append(configmenu, "&Config")
        MenuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(MenuBar)

        # Bind the various menu items to their callback methods.
        Bind(wx.EVT_MENU, OnOpenPatientPlan,     id=ID_FILE_OPEN_PATIENT_PLAN)
        Bind(wx.EVT_MENU, OnOpenPatientResults,  id=ID_FILE_OPEN_PATIENT_RESULTS)
        Bind(wx.EVT_MENU, OnSavePatientResults,  id=ID_FILE_SAVE_PATIENT_RESULTS)
        Bind(wx.EVT_MENU, OnQuit,        id=ID_FILE_QUIT)
        Bind(wx.EVT_MENU, OnLoadConfigs, id=ID_CONFIG_LOAD)
        Bind(wx.EVT_MENU, OnSaveConfigs, id=ID_CONFIG_SAVE)
        Bind(wx.EVT_MENU, OnToggleToolbar,  ToolbarToggle)
        Bind(wx.EVT_MENU, OnContents,    id=ID_HELP_CONTENTS)
        Bind(wx.EVT_MENU, OnAbout,       id=ID_HELP_ABOUT)

        # Create a toolbar object.
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)        
        
        toolbar.AddSimpleTool(ID_TOOL_OPEN_PATIENT_PLAN,
                              self.OpenPatientPlanToolBMP,
                              "Open Patient Plan", 
                              "Manually open a patient plan for analysis.")
        toolbar.AddSimpleTool(ID_TOOL_OPEN_PATIENT_RESULTS, 
                              self.OpenPatientResultsToolBMP,
                              "Open Patient Analysis Results", 
                              "Open analysis results for a patient.")
        toolbar.AddSimpleTool(ID_TOOL_SAVE_PATIENT_RESULTS,
                              self.SavePatientResultsToolBMP,
                              "Save Patient Analysis Results",
                              "Save Patient analysis results.")
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(ID_TOOL_START,
                              self.StartToolBMP,
                              "Start", 
                              "Start DICOM Listener and Dataset Score Display.")
        toolbar.AddSimpleTool(ID_TOOL_STOP,
                              self.StopToolBMP,
                              "Stop", 
                              "Stop DICOM Listener and Dataset Score Display.")
        toolbar.EnableTool(ID_TOOL_STOP, False)
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(ID_TOOL_QUIT,
                              self.QuitToolBMP,
                              "Quit",
                              "Quit the program.")

        # Display the toolbar.
        toolbar.Realize()

        # Bind the various toolbar buttons to their callback methods.
        Bind(wx.EVT_TOOL, OnOpenPatientPlan, id=ID_TOOL_OPEN_PATIENT_PLAN)
        Bind(wx.EVT_TOOL, OnOpenPatientResults,  id=ID_TOOL_OPEN_PATIENT_RESULTS)
        Bind(wx.EVT_TOOL, OnSavePatientResults,  id=ID_TOOL_SAVE_PATIENT_RESULTS)
        Bind(wx.EVT_TOOL, OnStart,   id=ID_TOOL_START)
        Bind(wx.EVT_TOOL, OnStop,    id=ID_TOOL_STOP)
        Bind(wx.EVT_TOOL, OnQuit,    id=ID_TOOL_QUIT)

        # Add a status bar.
        StatusBar = wx.CreateStatusBar()

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
