import wx

from SIC_GUI.Simulator.Run_Program.instruction_and_registers_history_panel import InstructionAndRegistersHistoryPanel
from SIC_GUI.Simulator.Run_Program.instruction_and_registers_panel import InstructionAndRegistersPanel


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        super(LeftPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # PANELS
        instruction_and_registers_panel = InstructionAndRegistersPanel(self)
        instruction_and_registers_history_panel = InstructionAndRegistersHistoryPanel(self)

        # LAYOUT
        vertical_box_sizer.Add(instruction_and_registers_panel, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10)
        vertical_box_sizer.Add(instruction_and_registers_history_panel, proportion=1, flag=wx.EXPAND)

        self.SetSizer(vertical_box_sizer)