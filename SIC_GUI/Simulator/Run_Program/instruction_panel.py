import wx


class InstructionPanel(wx.Panel):
    def __init__(self, parent):
        super(InstructionPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # CONTROLS

        txt_line_of_code = wx.TextCtrl(self, style=wx.TE_READONLY | wx.EXPAND)
        txt_line_of_code.SetMaxLength(71)
        txt_line_of_code.SetValue("2064     WLOOP     TD       OUTPUT                              E02079")

        # LAYOUT
        horizontal_box_sizer.Add(txt_line_of_code, proportion=1)

        self.SetSizer(horizontal_box_sizer)