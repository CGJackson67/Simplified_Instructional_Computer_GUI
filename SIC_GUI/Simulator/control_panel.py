import wx


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10)

        # CONTROLS
        lbl_program_file = wx.StaticText(self, label="Program File")
        fpc_program_file = wx.FilePickerCtrl(self, message="Select Object Code Program File", wildcard="*.obj")
        btn_load = wx.Button(self, label="Load")

        # LAYOUT
        grid_bag_sizer.Add(lbl_program_file, pos=(0, 0), flag=wx.EXPAND)
        grid_bag_sizer.Add(fpc_program_file, pos=(0, 1), span=(1, 8), flag=wx.EXPAND)
        grid_bag_sizer.AddGrowableCol(idx=1)
        grid_bag_sizer.Add(btn_load, pos=(0, 10), flag=wx.EXPAND | wx.ALIGN_RIGHT)

        self.SetSizer(grid_bag_sizer)
