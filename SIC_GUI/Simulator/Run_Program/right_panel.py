import wx


class RightPanel(wx.Panel):
    def __init__(self, parent):
        super(RightPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        txt_memory = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_box_sizer.Add(txt_memory, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        memory_static_box = wx.StaticBox(self, label="Memory")
        static_box_sizer = wx.StaticBoxSizer(memory_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)