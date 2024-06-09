import wx

from SIC_Simulator.sic_register_model import REGISTER_DICT, REGISTER_PC, dump_registers


class InstructionAndRegistersHistoryPanel(wx.Panel):
    def __init__(self, parent):
        super(InstructionAndRegistersHistoryPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.txt_instruction_and_registers_history = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.txt_instruction_and_registers_history.SetFont(MONOSPACED_FONT)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_instruction_and_registers_history, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        instruction_and_registers_history_static_box = wx.StaticBox(self, label="Instruction and Registers History")
        static_box_sizer = wx.StaticBoxSizer(instruction_and_registers_history_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)

    def print_assembly_listing_line(self, parsed_assembly_listing_dict):
        self.txt_instruction_and_registers_history.AppendText(parsed_assembly_listing_dict[REGISTER_DICT[REGISTER_PC].get_hex_string()] + "\n")

    def dump_registers(self):
        self.txt_instruction_and_registers_history.AppendText(dump_registers() + "\n\n")

    def initialize_txt_instruction_and_registers_history(self):
        self.txt_instruction_and_registers_history.Clear()