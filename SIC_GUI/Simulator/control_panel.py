import wx

from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10)

        # CONTROLS
        lbl_program_file = wx.StaticText(self, label="Program File")
        self.fpc_program_file = wx.FilePickerCtrl(self, path=SIC_DEFAULT_WORKING_DIRECTORY, message="Select Object Code Program File", wildcard="*.obj")
        self.fpc_program_file.GetTextCtrl().SetEditable(False)
        self.fpc_program_file.SetToolTip("Click Browse button to select *.obj program file")
        self.btn_load = wx.Button(self, label="Load")
        self.btn_load.SetToolTip("Click to load selected program file into memory")
        self.btn_load.Disable()

        # LAYOUT
        grid_bag_sizer.Add(lbl_program_file, pos=(0, 0), flag=wx.EXPAND)
        grid_bag_sizer.Add(self.fpc_program_file, pos=(0, 1), span=(1, 8), flag=wx.EXPAND)
        grid_bag_sizer.AddGrowableCol(idx=1)
        grid_bag_sizer.Add(self.btn_load, pos=(0, 10), flag=wx.EXPAND | wx.ALIGN_RIGHT)

        self.SetSizer(grid_bag_sizer)

    def enable_load_button(self):
        file_path = self.fpc_program_file.GetPath()

        if file_path == "":
            self.btn_load.Disable()
        else:
            self.btn_load.Enable()

    def get_file_path(self):
        return self.fpc_program_file.GetPath()
