import wx


class ObjectCodePanel(wx.Panel):
    def __init__(self, parent):
        super(ObjectCodePanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        txt_object_code = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_box_sizer.Add(txt_object_code, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_box_sizer)
