import wx


class OutputDevice05Panel(wx.Panel):
    def __init__(self, parent):
        super(OutputDevice05Panel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        txt_output = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_box_sizer.Add(txt_output, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        output_device_05_static_box = wx.StaticBox(self, label="Output Device 05")
        static_box_sizer = wx.StaticBoxSizer(output_device_05_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)