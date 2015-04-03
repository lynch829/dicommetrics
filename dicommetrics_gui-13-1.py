"""
DICOM Metrics
################################################################################

DICOM Metrics listens for dicom data sent to it from a radiation therapy treat-
ment planning system such as Eclipse or Pinnacle. With that data, it analyzes it
against an algorithm consisting of a set of scoring functions called metrics. 
The results for the currently sent dataset are displayed on. Options for saving 
the data are available as well as querying saved data.


:Author: Ali Kakakhel (alikakakhel@yahoo.com)
:License: GNU Public License Version 3



To Do:
--------------------------------------------------------------------------------

 0. Add the remaining features; Only the GUI is being built at the moment.
 2. Have the start and stop buttons switch/toggle between each other.
 4. Add tooltip to save message log button and menu items.
 5. Remove empty sapce when hiding the toolbar.
 5. Re-add the required space back when the toolbar is shown again.
 6. Add quick toggle-able configs such as: auto-anonymize, save to csv table,
    save to histograms sources.
 7. Add area above the metrics list to display info such as patient name, etc..
 8. Fix double clicking on border between the metrics list and message area.
 9. Fix no message on resize border between the metrics list and message area.
10. Add ability to query csv table for results.
11. Add ability to view histrograms.
"""

# Import various required libraries.
#import dicom, netdicom
import threading, wx


# Define a class of global variables and methods.
class g(object):
    dummy = 'variable'         # A dummy variable just there to act as a placeholder.
    

#==============================================================================#
#                                                                              #
#                                GUI Definition                                #
#                                                                              #
#==============================================================================#


class DicomMetrics(wx.Frame):
    
    def __init__(self):

        # Initialize the main frame (aka window).
        # Title the window 'DicoMetrics'.
        # Set the initial size to 1024x768.
        wx.Frame.__init__(self, None, -1, 'DICOM Metrics', size=(1024,768))   # Need to make it actually start of with the 1024x768 size.
        
        # Set the dicom listener to be paused on startup of the application.
        self.paused = True

        #
        # Collection of GUI element IDs.
        #
        self.ID_FILE_OPEN_PATIENT_PLAN     = 201
        self.ID_FILE_OPEN_PATIENT_RESULTS  = 202
        self.ID_FILE_SAVE_PATIENT_RESULTS  = 203
        self.ID_FILE_QUIT      = 204
        self.ID_CONFIG_LOAD    = 301
        self.ID_CONFIG_SAVE    = 302
        self.ID_TOOLBAR_TOGGLE = 303
        self.ID_HELP_CONTENTS  = 401
        self.ID_HELP_ABOUT     = 402

        self.ID_TOOL_OPEN_PATIENT_PLAN     = 10
        self.ID_TOOL_OPEN_PATIENT_RESULTS  = 20
        self.ID_TOOL_SAVE_PATIENT_RESULTS  = 30
        self.ID_TOOL_START = 40
        self.ID_TOOL_STOP  = 50
        self.ID_TOOL_QUIT  = 60

        self.ID_SPLITTER       = 70
        self.ID_SAVE_MESSAGES  = 80

        #
        # Collection of GUI BMPs.
        #
        # Make image objects for each of the icons on the toolbar:
        # save, start, stop, exit.
        #save_bmp = wx.Image('SaveTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #start_bmp = wx.Image('StartTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #stop_bmp  = wx.Image('StopTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #exit_bmp  = wx.Image('QuitTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.OpenPatientPlanMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (16,16))
        self.OpenPatientResultsMenuBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16,16))
        self.SavePatientResultsMenuBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16,16))
        self.QuitMenuBMP           = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16,16))
        self.LoadConfigsMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, (16,16))
        self.SaveConfigsMenuBMP    = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, (16,16))
        self.HelpContentsMenuBMP   = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_OTHER, (16,16))
        self.HelpAboutMenuBMP      = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16,16))
        
        self.OpenPatientPlanToolBMP    = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (32,32))
        self.OpenPatientResultsToolBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (32,32))
        self.SavePatientResultsToolBMP = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (32,32))
        #self.StartToolBMP  = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_OTHER, (32,32))
        #self.StopToolBMP   = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_OTHER, (32,32))
        self.StartToolBMP  = wx.Image('StartTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.StopToolBMP   = wx.Image('StopTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.QuitToolBMP   = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (32,32))

        # Run the method to create the main panel.
        self.create_main_panel()
        
        # Run the method to create the menu.
        self.create_menu()

        # Run the method to create the toolbar.
        self.create_toolbar()


    #
    # The method to create the menu.
    #
    def create_menu(self):

        # Create the file menu object and give it its menu items.
        filemenu = wx.Menu()
        FileOpenPatientPlan    = wx.MenuItem(filemenu, self.ID_FILE_OPEN_PATIENT_PLAN, 'Open Patient &Plan...\tCtrl+P')
        FileOpenPatientResults = wx.MenuItem(filemenu, self.ID_FILE_OPEN_PATIENT_RESULTS, 'Open Patient &Results\tCtrl+R')
        FileSavePatientResults = wx.MenuItem(filemenu, self.ID_FILE_SAVE_PATIENT_RESULTS, '&Save Patient Results\tCtrl+S')
        FileQuit               = wx.MenuItem(filemenu, self.ID_FILE_QUIT, '&Quit\tCtrl+Q')

        FileOpenPatientPlan.SetBitmap(self.OpenPatientPlanMenuBMP)
        FileOpenPatientPlan.SetBitmap(self.OpenPatientResultsMenuBMP)
        FileSavePatientResults.SetBitmap(self.SavePatientResultsMenuBMP)
        FileQuit.SetBitmap(self.QuitMenuBMP)

        filemenu.AppendItem(FileOpenPatientPlan)
        filemenu.AppendItem(FileOpenPatientResults)
        filemenu.AppendItem(FileSavePatientResults)
        filemenu.AppendSeparator()
        filemenu.AppendItem(FileQuit)

        # Create the config menu object and give it its menu items.
        configmenu = wx.Menu()
        LoadConfigs = wx.MenuItem(configmenu, self.ID_CONFIG_LOAD, '&Load Configuration')
        SaveConfigs = wx.MenuItem(configmenu, self.ID_CONFIG_SAVE, '&Save Configuration')
        
        LoadConfigs.SetBitmap(self.LoadConfigsMenuBMP)
        SaveConfigs.SetBitmap(self.SaveConfigsMenuBMP)
        
        configmenu.AppendItem(LoadConfigs)
        configmenu.AppendItem(SaveConfigs)
        configmenu.AppendSeparator()
        self.ToolbarToggle = configmenu.Append(self.ID_TOOLBAR_TOGGLE, 
                                               'Show Toolbar',
                                               'Toggle showing/hiding the toolbar', 
                                               kind=wx.ITEM_CHECK)
        configmenu.Check(self.ToolbarToggle.GetId(), True)

        # Create the help menu object and give it its menu items.
        helpmenu = wx.Menu()
        HelpContents = wx.MenuItem(helpmenu, self.ID_HELP_CONTENTS, '&Contents\tF1')
        HelpAbout    = wx.MenuItem(helpmenu, self.ID_HELP_ABOUT, '&About\tCtrl+A')

        HelpContents.SetBitmap(self.HelpContentsMenuBMP)
        HelpAbout.SetBitmap(self.HelpAboutMenuBMP)

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
        self.Bind(wx.EVT_MENU, self.OnOpenPatientPlan,     id=self.ID_FILE_OPEN_PATIENT_PLAN)
        self.Bind(wx.EVT_MENU, self.OnOpenPatientResults,  id=self.ID_FILE_OPEN_PATIENT_RESULTS)
        self.Bind(wx.EVT_MENU, self.OnSavePatientResults,  id=self.ID_FILE_SAVE_PATIENT_RESULTS)
        self.Bind(wx.EVT_MENU, self.OnQuit,        id=self.ID_FILE_QUIT)
        self.Bind(wx.EVT_MENU, self.OnLoadConfigs, id=self.ID_CONFIG_LOAD)
        self.Bind(wx.EVT_MENU, self.OnSaveConfigs, id=self.ID_CONFIG_SAVE)
        self.Bind(wx.EVT_MENU, self.OnToggleToolbar,  self.ToolbarToggle)
        self.Bind(wx.EVT_MENU, self.OnContents,    id=self.ID_HELP_CONTENTS)
        self.Bind(wx.EVT_MENU, self.OnAbout,       id=self.ID_HELP_ABOUT)

    #
    # The method to create the toolbar.
    #
    def create_toolbar(self):

        # Create a toolbar object.
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)        

        self.toolbar.AddSimpleTool(self.ID_TOOL_OPEN_PATIENT_PLAN,
                                   self.OpenPatientPlanToolBMP,
                                   "Open Patient Plan", 
                                   "Manually open a patient plan for analysis.")
        self.toolbar.AddSimpleTool(self.ID_TOOL_OPEN_PATIENT_RESULTS, 
                                   self.OpenPatientResultsToolBMP,
                                   "Open Patient Analysis Results", 
                                   "Open analysis results for a patient.")
        self.toolbar.AddSimpleTool(self.ID_TOOL_SAVE_PATIENT_RESULTS,
                                   self.SavePatientResultsToolBMP,
                                   "Save Patient Analysis Results",
                                   "Save Patient analysis results.")
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(self.ID_TOOL_START,
                                   self.StartToolBMP,
                                   "Start", 
                                   "Start DICOM Listener and Dataset Score Display.")
        self.toolbar.AddSimpleTool(self.ID_TOOL_STOP,
                                   self.StopToolBMP,
                                   "Stop", 
                                   "Stop DICOM Listener and Dataset Score Display.")
        self.toolbar.EnableTool(self.ID_TOOL_STOP, False)
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(self.ID_TOOL_QUIT,
                                   self.QuitToolBMP,
                                   "Quit",
                                   "Quit the program.")

        # Display the toolbar.
        self.toolbar.Realize()

        # Bind the various toolbar buttons to their callback methods.
        self.Bind(wx.EVT_TOOL, self.OnOpenPatientPlan, id=self.ID_TOOL_OPEN_PATIENT_PLAN)
        self.Bind(wx.EVT_TOOL, self.OnOpenPatientResults,  id=self.ID_TOOL_OPEN_PATIENT_RESULTS)
        self.Bind(wx.EVT_TOOL, self.OnSavePatientResults,  id=self.ID_TOOL_SAVE_PATIENT_RESULTS)
        self.Bind(wx.EVT_TOOL, self.OnStart,   id=self.ID_TOOL_START)
        self.Bind(wx.EVT_TOOL, self.OnStop,    id=self.ID_TOOL_STOP)
        self.Bind(wx.EVT_TOOL, self.OnQuit,    id=self.ID_TOOL_QUIT)

    #
    # The method to create the main panel.
    #
    def create_main_panel(self):

        # Create the split between the list of metrics and the statusbox.
        self.splitter = wx.SplitterWindow(self, self.ID_SPLITTER, style=wx.SP_BORDER)

        # Initialize a main panel for the application. This panel holds the
        # notebook widget and info box above it.
        self.MainPanel = wx.Panel(self.splitter, wx.ID_ANY)

        # Make a sizer to hold the info box and notebook widget.
        self.MainArea = wx.BoxSizer(wx.VERTICAL)

        # Initialize a boded box to hold information to be displayed.
        self.InfoBox = wx.StaticBox(self.MainPanel, label='')

        # Place a sizer in the info box to hold/arrange the info put in it.
        self.InfoSizer = wx.FlexGridSizer(rows=3, cols=4)

        # Create static text labels to hold info to be displayed.
        self.Label11 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label12 = wx.StaticText(self.InfoBox, -1, 'value')
        self.Label13 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label14 = wx.StaticText(self.InfoBox, -1, 'value')
        self.Label21 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label22 = wx.StaticText(self.InfoBox, -1, 'value')
        self.Label23 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label24 = wx.StaticText(self.InfoBox, -1, 'value')
        self.Label31 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label32 = wx.StaticText(self.InfoBox, -1, 'value')
        self.Label33 = wx.StaticText(self.InfoBox, -1, 'key:')
        self.Label34 = wx.StaticText(self.InfoBox, -1, 'value')

        # Add the static text labels to the flex grid sizer.
        self.InfoSizer.Add(self.Label11, 0, 0)
        self.InfoSizer.Add(self.Label12, 0, 0)
        self.InfoSizer.Add(self.Label13, 0, 0)
        self.InfoSizer.Add(self.Label14, 0, 0)
        self.InfoSizer.Add(self.Label21, 0, 0)
        self.InfoSizer.Add(self.Label22, 0, 0)
        self.InfoSizer.Add(self.Label23, 0, 0)
        self.InfoSizer.Add(self.Label24, 0, 0)
        self.InfoSizer.Add(self.Label31, 0, 0)
        self.InfoSizer.Add(self.Label32, 0, 0)
        self.InfoSizer.Add(self.Label33, 0, 0)
        self.InfoSizer.Add(self.Label34, 0, 0)

        # Initialize a notebook view to switch between the results view, algo-
        # oritm view, and DVH view.
        self.NoteView = wx.Notebook(self.MainPanel)

        # Create the panels that represent each tab/page of the notebook view.
        self.ResultsPanel = wx.Panel(self.NoteView, wx.ID_ANY)
        self.AlgPanel = wx.Panel(self.NoteView, wx.ID_ANY)
        self.DVHPanel = wx.Panel(self.NoteView, wx.ID_ANY)

        # Add the ListCtrl widget to the results panel. The ListCtrl widget
        # displays the list of metrics with their results.
        self.ListBox = wx.ListCtrl(self.ResultsPanel, -1, size=(728,400), style=wx.LC_REPORT|wx.LC_HRULES)

        # Add the column headers to the list of metrics.
        self.ListBox.InsertColumn(0, 'Name')
        self.ListBox.InsertColumn(1, 'Result')
        self.ListBox.InsertColumn(2, 'Score')
        self.ListBox.InsertColumn(3, 'Max Score')
        self.ListBox.InsertColumn(4, 'Rel Score')

        # Add a big text box to the algorithm panel. The text box widget
        # displays the currently loaded algorithm. In the future, it will also
        # allow editing the algorithm and updating the results.
        self.AlgBox = wx.TextCtrl(self.AlgPanel, -1, size=(728,400), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_DONTWRAP)

        # Add some content to the DVH panel.
        self.DummyText = wx.StaticText(self.DVHPanel, -1, 'This is will display the DVH of the current patient.', size=(728,400), style=wx.ALIGN_CENTRE_HORIZONTAL)
       
        # Add the pages to the notebook view.
        self.NoteView.AddPage(self.ResultsPanel, 'Results')
        self.NoteView.AddPage(self.AlgPanel, 'Algorithm')
        self.NoteView.AddPage(self.DVHPanel, 'DVH')

        # Add the notebook and info box to the main panel sizer and set the main
        # panel sizer on the main panel.
        self.MainArea.Add(self.InfoBox)
        self.MainArea.Add(self.NoteView)
        self.MainPanel.SetSizer(self.MainArea)
        
        # Make a panel to hold the status area sizer.
        self.StatusPanel = wx.Panel(self.splitter, wx.ID_ANY)

        # Make a sizer to hold the status message box and title areas.
        self.StatusArea = wx.BoxSizer(wx.VERTICAL)

        # Make a title area for the message area to put its label and
        # any other features such as a save button.
        self.StatusTitle = wx.BoxSizer(wx.HORIZONTAL)

        # Make a label to label the status message area.
        self.StatusLabel = wx.StaticText(self.StatusPanel, -1, ' Status Messages:')

        # Make a save button to save the message log.
        self.StatusSave = wx.BitmapButton(self.StatusPanel, self.ID_SAVE_MESSAGES, self.SavePatientResultsMenuBMP, size=(16,16), style=0)

        # Put the label and save button into the status title sizer.
        self.StatusTitle.Add(self.StatusLabel, 1)
        self.StatusTitle.Add(self.StatusSave, 0)

        # Make a TextCtrl representing the message area.
        self.StatusBox = wx.TextCtrl(self.StatusPanel, -1, size=(728,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_DONTWRAP)
        self.StatusBox.Disable()   # Disable the cursor in the statusbox.

        # Add the message and title area to the StatusArea sizer.
        self.StatusArea.Add(self.StatusTitle, 0)#, wx.EXPAND)
        self.StatusArea.Add(self.StatusBox, 1)#, wx.EXPAND)
        self.StatusPanel.SetSizer(self.StatusArea)
        
        # Add the ListCtl and sizer for the TextCtrl and its title to
        # the splitter window.
        self.splitter.SplitHorizontally(self.MainPanel, self.StatusPanel)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=self.ID_SPLITTER)
        self.Bind(wx.EVT_BUTTON, self.OnStatusSave, id=self.ID_SAVE_MESSAGES)


#==============================================================================#
#                                                                              #
#                               Callback Methods                               #
#                                                                              #
#==============================================================================#


    # The (callback) method to start the DICOM listener and automatic dataset
    # score display when the start button is pushed.
    # self.on_redraw_timer will automatically check the paused status and update
    # accordingly.
    def OnStart(self, event):
        self.paused = False
        self.toolbar.EnableTool(self.ID_TOOL_START, False)
        self.toolbar.EnableTool(self.ID_TOOL_STOP, True)
        self.AddStatus('Started waiting for data.')

    # The (callback) method to stop the DICOM listener and automatic dataset
    # score display when the stop button is pushed.
    # self.on_redraw_timer will automatically check the paused status and update
    # accordingly.
    def OnStop(self, event):
        self.paused = True
        self.toolbar.EnableTool(self.ID_TOOL_STOP, False)
        self.toolbar.EnableTool(self.ID_TOOL_START, True)
        self.AddStatus('Stopped waiting for data.')

    # The method to run when the split is adjusted.
    def OnSize(self, event):
        size = self.GetSize()
        #self.splitter.SetSashPosition(size.y / 3)
        event.Skip()
        self.AddStatus('Resized the splitter window.')

    # The method to run when the split is double-clicked. 
    def OnDoubleClick(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.y / 3)
        self.AddStatus('Double clicked the split.')
        # This just makes the split disappear. What I want it to do is to reset
        # the split to its original size which is a 67-33 split for now.

    # The method to run when the status message save button is clicked.
    def OnStatusSave(self, event):
        self.AddStatus('Pressed the button to save the messages log.')
    
    # The (callback) method to (manually) open a patient plan as opposed to just
    # automatically opening any plan that is sent to DICOM Metrics.
    def OnOpenPatientPlan(self, event):
        self.AddStatus('Open the Open Patient Plan Dialog Box')

    # The (callback) method to open a patient's results.
    def OnOpenPatientResults(self, event):
        self.AddStatus('Open the Open Patient Results Dialog Box')

    # The (callback) method to save the current patient's results.
    # Save to main csv table and histograms sources.
    def OnSavePatientResults(self, event):
        self.AddStatus('Open the Save Patient Results Dialog Box')

    # The (callback) method to close the window when the exit button is pushed.
    # Makes sure that the DICOM listener has been turned off before it exits.
    def OnQuit(self, event):
        if not self.paused: self.OnStop(event)
        self.AddStatus('Exiting the program.')
        self.Destroy()

    # The (callback) method to load a configuration file.
    def OnLoadConfigs(self, event):
        self.AddStatus('Open the load configuration dialog box.')

    # The (callback) method to save the current configuration to a file.
    def OnSaveConfigs(self, event):
        self.AddStatus('Open the save configuration dialog box.')

    # The (callback) method to toggle viewing the toolbar.
    def OnToggleToolbar(self, event):
    
        if self.ToolbarToggle.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    # The (callback) method to open the table of contents for the help system.
    def OnContents(self, event):
        self.AddStatus('Open the help\'s table of conents.')

    # The (callback) method to open a message box giving information about
    # DICOM Metrics such as its name, version, principal contributor(s), 
    # license, etc..
    def OnAbout(self, event):
        self.AddStatus('Open the about message box.')

    # The method used to append another status message to the statusbox.
    # The method adds a newline character to the end before appending.
    def AddStatus(self, msg):
        self.StatusBox.AppendText(msg + '\n')
    

#==============================================================================#
#                                                                              #
#                                Run Main Loop                                 #
#                                                                              #
#==============================================================================#


if __name__ == '__main__':
    # Create an object for the application gui.
    app = wx.App()      

    # Create a frame object for the graphing frame.
    app.frame = DicomMetrics()    

    # Make the graph frame visible.
    app.frame.Show()            

    # Run the mainloop to handle all the application events.
    app.MainLoop()              

# END
