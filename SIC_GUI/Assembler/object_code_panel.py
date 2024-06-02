import wx


class ObjectCodePanel(wx.Panel):
    def __init__(self, parent):
        super(ObjectCodePanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        self.txt_object_code = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        monospace_font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.txt_object_code.SetFont(monospace_font)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_object_code, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_box_sizer)

    def load_object_code_file(self, object_code_file_path):
        self.txt_object_code.LoadFile(object_code_file_path)

    def clear(self):
        self.txt_object_code.Clear()
