import wx


class LoadStatusPanel(wx.Panel):
    def __init__(self, parent):
        super(LoadStatusPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        txt_load_status = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_box_sizer.Add(txt_load_status, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_box_sizer)
