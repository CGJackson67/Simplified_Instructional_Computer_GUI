import wx


class InstructionPanel(wx.Panel):
    def __init__(self, parent):
        super(InstructionPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.txt_line_of_code = wx.TextCtrl(self, style=wx.TE_READONLY | wx.EXPAND)
        self.txt_line_of_code.SetMaxLength(71)
        self.txt_line_of_code.SetFont(MONOSPACED_FONT)

        # LAYOUT
        horizontal_box_sizer.Add(self.txt_line_of_code, proportion=1)

        self.SetSizer(horizontal_box_sizer)


    def update_instruction_text_ctrl(self, line_of_code):
        self.txt_line_of_code.SetValue(line_of_code)