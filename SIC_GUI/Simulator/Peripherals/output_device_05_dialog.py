import wx

from SIC_Utilities.sic_converter import dec_to_hex_string


class OutputDevice05Dialog(wx.Dialog):
    def __init__(self, parent, title, OUTPUT_DEVICE_05_INTERFACE):
        super(OutputDevice05Dialog, self).__init__(parent, title=title)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.txt_input = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.txt_input.SetFont(MONOSPACED_FONT)
        self.txt_input.SetValue(OUTPUT_DEVICE_05_INTERFACE)
        self.btn_acknowledge = wx.Button(self, label="Acknowledge")
        self.btn_acknowledge.SetToolTip("Click to acknowledge and close dialog")

        # LAYOUT
        vertical_layout.Add(self.txt_input, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        vertical_layout.Add(self.btn_acknowledge, proportion=0, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)

        self.SetSizer(vertical_layout)
        # self.Fit()

        # BIND EVENTS
        self.Bind(wx.EVT_BUTTON, self.on_button)

    def on_button(self, event):
        self.EndModal(wx.ID_OK)