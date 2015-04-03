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

 1. Only the GUI is being built at the moment.
 2. Replace the status bar with a message box.
 3. Allow saving the messages from the message box.
 4. Have the start and stop buttons switch/toggle between each other.
 0. Add the remaining features.
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

        # Run the method to create the main panel.
        self.create_main_panel()
        
        # Run the method to create the menu.
        self.create_menu()

        # Run the method to create the toolbar.
        self.create_toolbar()


    # The method to create the menu.
    def create_menu(self):
        
        ID_EXIT = 200

        # Create the file menu object and give it its menu items.
        # The only menu item is Exit for now.
        filemenu= wx.Menu()
        filemenu.Append(ID_EXIT, "E&xit", "Terminate the program")

        # Create the config menu object and give it its menu items.
        # There are no menu items for now.
        configmenu = wx.Menu()

        # Create the help menu object and give it its menu items.
        # There are no menu items for now.
        helpmenu = wx.Menu()

        # Create the menubar object and give it the above created menu objects.
        # There is only File, Config, and Help as available menus so far.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

    # The method to create the toolbar.
    def create_toolbar(self):

        # Create a toolbar object.
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)

        # Define the icon size to be used.
        IconSize = (48,48)

        # Set the toolbar icon size to the above defined size.
        toolbar.SetToolBitmapSize(IconSize)

        # Make image objects for each of the icons on the toolbar:
        # start, stop, exit.
        start_bmp = wx.Image('StartTool.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        stop_bmp  = wx.Image('StopTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        exit_bmp  = wx.Image('QuitTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        # Add the start button to the toolbar.
        # Give the button an id: 20, an image object: start_bmp, tooltip: 'Start',
        # and a statusbar text: 'Start DICOM Listener and Dataset Score Display.'.
        toolbar.AddSimpleTool(20, start_bmp, "Start",
                              "Start DICOM Listener and Dataset Score Display.")

        # Bind the start button to the self.on_start (callback) method.
        self.Bind(wx.EVT_TOOL, self.OnStart, id=20)

        # Add the stop button to the toolbar.
        # Give the button an id: 30, an image object: stop_bmp, tooltip: 'Stop',
        # and a statusbar text: 'Stop DICOM Listener and Dataset Score Display.'.
        toolbar.AddSimpleTool(30, stop_bmp, "Stop", 
                              "Stop DICOM Listener and Dataset Score Display.")

        # Bind the stop button to the self.on_stop (callback) method.
        self.Bind(wx.EVT_TOOL, self.OnStop, id=30)

        # Add the exit button to the toolbar.
        # Give the button an id: 40, an image object: exit_bmp, tooltip: 'Exit',
        # and a statusbar text: 'Exit the program.'.
        toolbar.AddSimpleTool(40, exit_bmp, "Exit", "Exit the program.")

        # Bind the exit button to the self.on_exit (callback) method.
        self.Bind(wx.EVT_TOOL, self.OnExit, id=40)

        # Display the toolbar.
        toolbar.Realize()

    # The method to create the main panel.
    def create_main_panel(self):

        self.ID_SPLITTER = 300

        # Create the split between the list of metrics and the statusbox.
        self.splitter = wx.SplitterWindow(self, self.ID_SPLITTER, style=wx.SP_BORDER)

        # Make a ListCtrl representing the list of metrics.
        self.ListBox = wx.ListCtrl(self.splitter, -1, size=(728,400), style=wx.LC_REPORT|wx.LC_HRULES)
        
        # Make a sizer to hold the status message box and title areas.
        self.StatusArea = wx.BoxSizer(wx.VERTICAL)

        # Make a TextCtrl representing the message area.
        self.StatusBox = wx.TextCtrl(self.StatusArea, -1, size=(728,100), style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_DONTWRAP)
        self.StatusBox.Disable()   # Disable the cursor in the statusbox.

        # Make a title area for the message area to put its label and
        # any other features such as a save button.
        self.StatusTitle = wx.BoxSizer(wx.HORIZONTAL)

        # Make a label to label the status message area.
        self.StatusLabel = wx.StaticText(self.splitter, -1, 'Status Messages:')

        # Make a save button to save the message log.
        save_bmp  = wx.Image('SaveTool.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.StatusSave = wx.BitmapButton(self.splitter, -1, save_bmp, size=(24,24))
        self.StatusSave.Bind(wx.EVT_BUTTON, self.OnStatusSave)

        # Put the label and save button into the status title sizer.
        self.StatusTitle.Add(self.StatusLabel, 1, wx.EXPAND)
        self.StatusTitle.Add(self.StatusSave, 1, wx.EXPAND)
        self.splitter.SetSizer(self.StatusTitle)

        # Add the message and title area to the StatusArea sizer.
        self.StatusArea.Add(self.StatusTitle, 1, wx.EXPAND)
        self.StatusArea.Add(self.StatusBox, 1, wx.EXPAND)
        self.splitter.SetSizer(self.StatusArea)
        
        # Add the ListCtl and sizer for the TextCtrl and its title to
        # the splitter window.
        self.splitter.SplitHorizontally(self.ListBox, self.StatusArea)

        # Add the column headers to the list of metrics.
        self.ListBox.InsertColumn(0, 'Name')
        self.ListBox.InsertColumn(1, 'Result')
        self.ListBox.InsertColumn(2, 'Score')
        self.ListBox.InsertColumn(3, 'Max Score')

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=self.ID_SPLITTER)


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
        self.AddStatus('Started waiting for data...')

    # The (callback) method to stop the DICOM listener and automatic dataset
    # score display when the stop button is pushed.
    # self.on_redraw_timer will automatically check the paused status and update
    # accordingly.
    def OnStop(self, event):
        self.paused = True
        self.AddStatus('Stopped waiting for data...')

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
        # the split to its original size which is a 66-33 split for now.

    # The method to run when the status message save button is clicked.
    def OnStatusSave(self, event):
        self.AddStatus('Pressed the button to save the messages log.')
    
    # The (callback) method to close the window when the exit button is pushed.
    # Makes sure that the DICOM listener has been turned off before it exits.
    def OnExit(self, event):
        self.OnStop(event)
        self.AddStatus('Exiting the program.')
        self.Destroy()

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
