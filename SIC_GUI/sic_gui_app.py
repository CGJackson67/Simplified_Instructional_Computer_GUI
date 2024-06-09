import wx

from SIC_GUI.Assembler.assembler_panel import AssemblerPanel
from SIC_GUI.Simulator.simulator_panel import SimulatorPanel


class SICGUIFrame(wx.Frame):
    def __init__(self, parent, title):
        super(SICGUIFrame, self).__init__(parent, title=title, size=(1250, 800))

        menubar = wx.MenuBar()

        menu_file = wx.Menu()
        menu_item_exit = wx.MenuItem(menu_file, 103, "E&xit")

        menu_file.Append(menu_item_exit)
        menubar.Append(menu_file, "&File")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.menu_handler)
        self.Bind(wx.EVT_CLOSE, self.close_handler)

        # NOTEBOOK
        notebook_sic = wx.Notebook(self)

        tab_assembler = AssemblerPanel(notebook_sic)
        notebook_sic.AddPage(tab_assembler, "Assembler")

        tab_simulator = SimulatorPanel(notebook_sic)
        notebook_sic.AddPage(tab_simulator, "Simulator")

        # Center the app on the monitor when it opens
        self.Centre()
        self.Show(True)

    def menu_handler(self, event):
        if event.GetId() == 103:
            exit_dialog = wx.MessageDialog(None, "Do you want to exit?", "Exit Confirm", wx.YES_NO | wx.ICON_QUESTION)
            confirm_response = exit_dialog.ShowModal()

            if confirm_response == wx.ID_YES:
                self.Destroy()

    def close_handler(self, event):
        exit_dialog = wx.MessageDialog(None, "Do you want to exit?", "Exit Confirm", wx.YES_NO | wx.ICON_QUESTION)
        confirm_response = exit_dialog.ShowModal()

        if confirm_response == wx.ID_YES:
            self.Destroy()


class SICGUIApp(wx.App):
    def OnInit(self):
        sic_gui_frame = SICGUIFrame(parent=None, title="Simplified Instructional Computer")
        sic_gui_frame.Show()

        return True


sic_gui_app = SICGUIApp()
sic_gui_app.MainLoop()
