import wx

from SIC_GUI.Simulator.Run_Program.left_panel import LeftPanel
from SIC_GUI.Simulator.Run_Program.right_panel import RightPanel


class RunProgramPanel(wx.Panel):
    def __init__(self, parent):
        super(RunProgramPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = LeftPanel(self)
        right_panel = RightPanel(self)

        # LAYOUT
        horizontal_box_sizer.Add(left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        horizontal_box_sizer.Add(right_panel, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

        self.SetSizer(horizontal_box_sizer)
