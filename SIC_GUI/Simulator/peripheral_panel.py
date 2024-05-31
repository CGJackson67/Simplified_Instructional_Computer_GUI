import wx

from SIC_GUI.Simulator.Peripherals.input_device_f1_panel import InputDeviceF1Panel
from SIC_GUI.Simulator.Peripherals.output_device_05_panel import OutputDevice05Panel


class PeripheralsPanel(wx.Panel):
    def __init__(self, parent):
        super(PeripheralsPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = InputDeviceF1Panel(self)
        right_panel = OutputDevice05Panel(self)

        # LAYOUT
        horizontal_box_sizer.Add(left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        horizontal_box_sizer.Add(right_panel, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

        self.SetSizer(horizontal_box_sizer)