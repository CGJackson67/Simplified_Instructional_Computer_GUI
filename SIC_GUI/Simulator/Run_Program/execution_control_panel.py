import wx


class ExecutionControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ExecutionControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        btn_end = wx.Button(self, label="End")
        btn_run = wx.Button(self, label="Run")
        btn_step = wx.Button(self, label="Step")

        # LAYOUT
        grid_bag_sizer.Add(btn_end, flag=wx.ALIGN_RIGHT, pos=(0, 0))
        grid_bag_sizer.Add(btn_run, flag=wx.ALIGN_CENTER, pos=(0, 1))
        grid_bag_sizer.Add(btn_step, flag=wx.ALIGN_RIGHT, pos=(0, 2))

        self.SetSizer(grid_bag_sizer)