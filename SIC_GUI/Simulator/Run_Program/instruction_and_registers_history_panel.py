import wx


class InstructionAndRegistersHistoryPanel(wx.Panel):
    def __init__(self, parent):
        super(InstructionAndRegistersHistoryPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        txt_instruction_history = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # LAYOUT
        vertical_box_sizer.Add(txt_instruction_history, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        instruction_and_registers_history_static_box = wx.StaticBox(self, label="Instruction and Registers History")
        static_box_sizer = wx.StaticBoxSizer(instruction_and_registers_history_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)
