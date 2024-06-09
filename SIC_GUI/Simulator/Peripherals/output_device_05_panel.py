import wx


class OutputDevice05Panel(wx.Panel):
    def __init__(self, parent):
        super(OutputDevice05Panel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.txt_output = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.txt_output.SetFont(MONOSPACED_FONT)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_output, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        output_device_05_static_box = wx.StaticBox(self, label="Output Device 05")
        static_box_sizer = wx.StaticBoxSizer(output_device_05_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)

    def initialize(self):
        self.txt_output.Clear()
