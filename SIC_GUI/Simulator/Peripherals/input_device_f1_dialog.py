import wx

from SIC_Utilities.sic_converter import dec_to_hex_string


class InputDeviceF1Dialog(wx.Dialog):
    def __init__(self, parent, title, is_in_EOF_state):
        super(InputDeviceF1Dialog, self).__init__(parent, title=title)

        self.read_device_input = None

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.lbl_info = wx.StaticText(self, label="Input one character, Newline, or End of File and press Enter")
        self.txt_input = wx.TextCtrl(self)
        self.txt_input.SetFont(MONOSPACED_FONT)
        self.txt_input.SetMaxLength(1)
        self.btn_clear = wx.Button(self, label="Clear")
        self.btn_clear.SetToolTip("Click to clear input")
        self.btn_enter = wx.Button(self, label="Enter")
        self.btn_enter.SetToolTip("Click to input character")
        self.btn_newline = wx.Button(self, label="Newline")
        self.btn_newline.SetToolTip("Click to input a newline character")
        self.btn_end_of_record = wx.Button(self, label="End of Record")
        self.btn_end_of_record.SetToolTip("Click to input an end of record")
        self.btn_end_of_file = wx.Button(self, label="End of File")
        self.btn_end_of_file.SetToolTip("Click to input an end of file")

        # LAYOUT
        grid_bag_sizer.Add(self.lbl_info, flag=wx.ALIGN_LEFT | wx.EXPAND, pos=(0, 0), span=(1, 4))
        grid_bag_sizer.Add(self.txt_input, flag=wx.EXPAND, pos=(1, 0), span=(1, 3))
        grid_bag_sizer.Add(self.btn_clear, pos=(1, 3))
        grid_bag_sizer.Add(self.btn_end_of_file, pos=(2, 0))
        grid_bag_sizer.Add(self.btn_end_of_record, pos=(2, 1))
        grid_bag_sizer.Add(self.btn_newline, pos=(2, 2))
        grid_bag_sizer.Add(self.btn_enter, pos=(2, 3))

        # SIZER
        vertical_layout = wx.BoxSizer(wx.VERTICAL)

        # LAYOUT
        vertical_layout.Add(grid_bag_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.SetSizer(vertical_layout)
        self.Fit()

        # SET STATE
        self.txt_input.Enable()
        self.btn_enter.Disable()
        self.btn_newline.Enable()
        self.btn_end_of_file.Disable()
        self.btn_end_of_record.Disable()
        if is_in_EOF_state:
            self.lbl_info.SetLabelText("Input one character, Newline, or End of File and press Enter")
            self.btn_end_of_file.Enable()
        else:
            self.lbl_info.SetLabelText("Input one character, Newline, or End of Record and press Enter")
            self.btn_end_of_record.Enable()

        # BIND EVENTS
        self.Bind(wx.EVT_BUTTON, self.on_button)
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_button(self, event):
        button_label = event.GetEventObject().GetLabel()

        match button_label:
            case "End of File":
                self.txt_input.SetMaxLength(3)
                self.txt_input.SetValue("EOF")
                self.txt_input.SetEditable(False)
            case "End of Record":
                self.txt_input.SetMaxLength(3)
                self.txt_input.SetValue("EOR")
                self.txt_input.SetEditable(False)
            case "Newline":
                self.txt_input.SetMaxLength(2)
                self.txt_input.SetValue("\\n")
                self.txt_input.SetEditable(False)
            case "Clear":
                self.txt_input.SetMaxLength(1)
                self.txt_input.Clear()
                self.txt_input.SetEditable(True)
            case "Enter":
                match self.txt_input.GetValue():
                    case "EOF":
                        self.read_device_input = "00"
                    case "EOR":
                        self.read_device_input = "00"
                    case "\\n":
                        self.read_device_input = "0A"
                    case _:
                        self.read_device_input = self.txt_input.GetValue()
                        dec_ascii_value = ord(self.read_device_input)
                        self.read_device_input = dec_to_hex_string(dec_ascii_value)

                self.EndModal(wx.ID_OK)

    def on_text(self, event):
        if self.txt_input.GetValue() == "":
            self.btn_enter.Disable()
        else:
            self.btn_enter.Enable()
            self.btn_enter.SetDefault()

    def on_close(self, event):
        button_label = event.GetEventObject().GetLabel()
        if not button_label == "Enter":
            event.Veto()

