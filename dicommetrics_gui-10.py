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
 4. Add the remaining features.
"""

# Import various required libraries.
import dicom, netdicom, threading, wx


# Define a class of global variables and methods.
class g(object):
    dummy = 'variable'         # A dummy variable just there to act as a placeholder.
    

# Define a class to create and initialize all the various components of the main
# frame of the application.
class DicomMetrics(wx.Frame):
    
    def __init__(self):

        # Initialize the main frame (aka window).
        # Title the window 'DicoMetrics'.
        # Set the initial size to 1024x768.
        wx.Frame.__init__(self, None, -1, 'DICOM Metrics', size=(1024,768))   # Need to make it actually start of with the 1024x768 size.
        
        # Set the dicom listener to be paused on startup of the application.
        self.paused = True
        
        # Run the method to create the menu.
        self.create_menu()

        # Run the method to create the toolbar.
        self.create_toolbar()

        # Run the method to create the status bar.
        # Replace the status bar with a message box.
        self.create_status_bar()

        # Run the method to create the main panel.
        self.create_main_panel()
        
        # Set a timer for when to refresh everything and what to do when refreshing.
        # Refresh every g.IntraGatheringPeriod milliseconds.
        # Run self.on_redraw_timer when refreshing.
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
        self.redraw_timer.Start(g.IntraGatheringPeriod)

    # The method to create the menu.
    def create_menu(self):
        pass

    # The method to create the toolbar.
    def create_toolbar(self):

        # Create a toolbar object.
        # Alternative flags: wx.TB_FLAT | wx.TB_HORZ_LAYOUT
        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

        # Define the icon size to be used.
        IconSize = (64,64)

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
        self.Bind(wx.EVT_TOOL, self.on_start, id=20)

        # Add the stop button to the toolbar.
        # Give the button an id: 30, an image object: stop_bmp, tooltip: 'Stop',
        # and a statusbar text: 'Stop DICOM Listener and Dataset Score Display.'.
        toolbar.AddSimpleTool(30, stop_bmp, "Stop", 
                              "Stop DICOM Listener and Dataset Score Display.")

        # Bind the stop button to the self.on_stop (callback) method.
        self.Bind(wx.EVT_TOOL, self.on_stop, id=30)

        # Add the exit button to the toolbar.
        # Give the button an id: 40, an image object: exit_bmp, tooltip: 'Exit',
        # and a statusbar text: 'Exit the program.'.
        toolbar.AddSimpleTool(40, exit_bmp, "Exit", "Exit the program.")

        # Bind the exit button to the self.on_exit (callback) method.
        self.Bind(wx.EVT_TOOL, self.on_exit, id=40)

        # Display the toolbar.
        toolbar.Realize()

    # The method to create the main panel.
    def create_main_panel(self):

        # Initialize the main panel by creating the panel object.
        self.panel = wx.Panel(self)

        # Create a sizer to put the list of metric results and status
        # messages into.
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Create a list or table widget and add it to the sizer.
        self.MetricsList = wx.LisCtrl(self.panel, wx.ID_ANY, size=(728,400), style = wx.LC_REPORT|wx.LC_HRULES)
        self.vbox.Add(self.MetricsList, 1, wx.EXPAND)

        # Create a text control widget to house status messages, etc.,
        # disable the cursor within it, and add it to the sizer.
        self.StatusBox = wx.TextCtrl(self.panel, wx.ID_ANY, size=(728,100), style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_DONTWRAP)
        self.StatusBox.Disable()
        self.vbox.Add(self.StatusBox, 1, wx.EXPAND)

        # Set the sizer to make sure the components expand to fit.
        self.SetSizerAndFit(vbox)

    # The (callback) method to start the DICOM listener and automatic dataset
    # score display when the start button is pushed.
    # self.on_redraw_timer will automatically check the paused status and update
    # accordingly.
    def on_start(self, event):
        self.paused = False
        self.statusbar.SetStatusText("Waiting for data...")

    # The (callback) method to stop the DICOM listener and automatic dataset
    # score display when the stop button is pushed.
    # self.on_redraw_timer will automatically check the paused status and update
    # accordingly.
    def on_stop(self, event):
        self.paused = True
        self.statusbar.SetStatusText("Stopped gathering data...")
        
    # The method to run everytime the redraw timer triggers.
    def on_redraw_timer(self, event):

        # If paused do not add data, but still do other things to update in res-
        # ponce to any scale modifications, or other changes.
    
    # The (callback) method to close the window when the exit button is pushed.
    # Makes sure that the DICOM listener has been turned off before it exits.
    def on_exit(self, event):
        self.on_stop()
        self.Destroy()

    # The method used to append another status message to the statusbox.
    # The method adds a newline character to the end before appending.
    def add_status(self, msg):
        self.StatusBox.AppendText(msg + '\n')
    


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
