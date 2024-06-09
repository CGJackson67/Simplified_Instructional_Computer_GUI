import wx

from SIC_Assembler.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10)

        # CONTROLS
        self.lbl_program_file = wx.StaticText(self, label="Program File")
        self.fpc_program_file = wx.FilePickerCtrl(self, path=SIC_DEFAULT_WORKING_DIRECTORY, message="Select Assembly Program File", wildcard="*.asm")
        self.fpc_program_file.GetTextCtrl().SetEditable(False)
        self.fpc_program_file.SetToolTip("Click Browse button to select *.asm program file")

        self.btn_assemble = wx.Button(self, label="Assemble")
        self.btn_assemble.SetToolTip("Click to assemble selected program file")
        self.btn_assemble.Disable()

        # LAYOUT
        grid_bag_sizer.Add(self.lbl_program_file, pos=(0, 0), flag=wx.EXPAND)
        grid_bag_sizer.Add(self.fpc_program_file, pos=(0, 1), span=(1, 8), flag=wx.EXPAND)
        grid_bag_sizer.AddGrowableCol(idx=1)
        grid_bag_sizer.Add(self.btn_assemble, pos=(0, 10), flag=wx.EXPAND | wx.ALIGN_RIGHT)

        self.SetSizer(grid_bag_sizer)

    def enable_assemble_button(self):
        file_path = self.fpc_program_file.GetPath()

        if file_path == "":
            self.btn_assemble.Disable()
        else:
            self.btn_assemble.Enable()

    def get_file_path(self):
        return self.fpc_program_file.GetPath()

