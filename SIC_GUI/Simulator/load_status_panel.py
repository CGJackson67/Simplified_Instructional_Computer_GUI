import wx


class LoadStatusPanel(wx.Panel):
    def __init__(self, parent):
        super(LoadStatusPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.txt_load_status = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.txt_load_status.SetFont(MONOSPACED_FONT)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_load_status, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_box_sizer)

    def set_load_status(self, load_status, load_error=False):
        self.txt_load_status.SetForegroundColour(wx.BLACK)

        if load_error:
            self.txt_load_status.SetForegroundColour(wx.RED)

        self.txt_load_status.AppendText(text=load_status)

    def load_object_code_file(self, object_code_file_path):
        self.txt_load_status.SetForegroundColour(wx.BLACK)

        self.txt_load_status.LoadFile(object_code_file_path)
        self.txt_load_status.AppendText(("\nObject Code File Ready\n"))
        self.txt_load_status.AppendText(("Click the Load button to load program into memory and enable Run Program and Peripherals tabs\n"))
