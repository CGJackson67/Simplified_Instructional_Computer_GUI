import wx

from SIC_GUI.Simulator.Run_Program.execution_control_panel import ExecutionControlPanel
from SIC_GUI.Simulator.Run_Program.instruction_panel import InstructionPanel


class InstructionAndRegistersPanel(wx.Panel):
    def __init__(self, parent):
        super(InstructionAndRegistersPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # PANELS
        instruction_panel = InstructionPanel(self)
        execution_control_panel = ExecutionControlPanel(self)

        # CONTROLS
        lbl_register_a = wx.StaticText(self, label="REGISTER  A:")
        lbl_register_x = wx.StaticText(self, label="REGISTER  X:")
        lbl_register_l = wx.StaticText(self, label="REGISTER  L:")
        lbl_register_pc = wx.StaticText(self, label="REGISTER PC:")
        lbl_register_sw = wx.StaticText(self, label="REGISTER SW:")

        lbl_hex_a = wx.StaticText(self, label="HEX")
        lbl_bin_a = wx.StaticText(self, label="BIN")
        lbl_hex_x = wx.StaticText(self, label="HEX")
        lbl_bin_x = wx.StaticText(self, label="BIN")
        lbl_hex_l = wx.StaticText(self, label="HEX")
        lbl_bin_l = wx.StaticText(self, label="BIN")
        lbl_hex_pc = wx.StaticText(self, label="HEX")
        lbl_bin_pc = wx.StaticText(self, label="BIN")
        lbl_hex_sw = wx.StaticText(self, label="HEX")
        lbl_bin_sw = wx.StaticText(self, label="BIN")

        HEX_TEXT_CTRL_WIDTH = 65

        txt_register_a_hex = wx.TextCtrl(self, style=wx.TE_READONLY, size=(HEX_TEXT_CTRL_WIDTH, -1))
        txt_register_a_hex.SetMaxLength(8)
        txt_register_a_hex.SetValue("EE EE EE")
        txt_register_x_hex = wx.TextCtrl(self, style=wx.TE_READONLY, size=(HEX_TEXT_CTRL_WIDTH, -1))
        txt_register_x_hex.SetMaxLength(8)
        txt_register_l_hex = wx.TextCtrl(self, style=wx.TE_READONLY, size=(HEX_TEXT_CTRL_WIDTH, -1))
        txt_register_l_hex.SetMaxLength(8)
        txt_register_pc_hex = wx.TextCtrl(self, style=wx.TE_READONLY, size=(HEX_TEXT_CTRL_WIDTH, -1))
        txt_register_pc_hex.SetMaxLength(8)
        txt_register_sw_hex = wx.TextCtrl(self, style=wx.TE_READONLY, size=(HEX_TEXT_CTRL_WIDTH, -1))
        txt_register_sw_hex.SetMaxLength(8)

        BIN_TEXT_CTRL_WIDTH = 200

        txt_register_a_bin = wx.TextCtrl(self, style=wx.TE_READONLY, size=(BIN_TEXT_CTRL_WIDTH, -1))
        txt_register_a_bin.SetMaxLength(31)
        txt_register_a_bin.SetValue("0000 0000  0000 0000  0000 0000")
        txt_register_x_bin = wx.TextCtrl(self, style=wx.TE_READONLY, size=(BIN_TEXT_CTRL_WIDTH, -1))
        txt_register_x_bin.SetMaxLength(31)
        txt_register_l_bin = wx.TextCtrl(self, style=wx.TE_READONLY, size=(BIN_TEXT_CTRL_WIDTH, -1))
        txt_register_l_bin.SetMaxLength(31)
        txt_register_pc_bin = wx.TextCtrl(self, style=wx.TE_READONLY, size=(BIN_TEXT_CTRL_WIDTH, -1))
        txt_register_pc_bin.SetMaxLength(31)
        txt_register_sw_bin = wx.TextCtrl(self, style=wx.TE_READONLY, size=(BIN_TEXT_CTRL_WIDTH, -1))
        txt_register_sw_bin.SetMaxLength(31)

        # LAYOUT
        grid_bag_sizer.Add(instruction_panel, flag=wx.EXPAND, pos=(0, 0), span=(0, 5))

        grid_bag_sizer.Add(lbl_register_a, pos=(1, 0))
        grid_bag_sizer.Add(lbl_hex_a, pos=(1, 1))
        grid_bag_sizer.Add(txt_register_a_hex, pos=(1, 2))
        grid_bag_sizer.Add(lbl_bin_a, pos=(1, 3))
        grid_bag_sizer.Add(txt_register_a_bin, pos=(1, 4))
        grid_bag_sizer.AddGrowableCol(idx=4)

        grid_bag_sizer.Add(lbl_register_x, pos=(2, 0))
        grid_bag_sizer.Add(lbl_hex_x, pos=(2, 1))
        grid_bag_sizer.Add(txt_register_x_hex, pos=(2, 2))
        grid_bag_sizer.Add(lbl_bin_x, pos=(2, 3))
        grid_bag_sizer.Add(txt_register_x_bin, pos=(2, 4))

        grid_bag_sizer.Add(lbl_register_l, pos=(3, 0))
        grid_bag_sizer.Add(lbl_hex_l, pos=(3, 1))
        grid_bag_sizer.Add(txt_register_l_hex, pos=(3, 2))
        grid_bag_sizer.Add(lbl_bin_l, pos=(3, 3))
        grid_bag_sizer.Add(txt_register_l_bin, pos=(3, 4))

        grid_bag_sizer.Add(lbl_register_pc, pos=(4, 0))
        grid_bag_sizer.Add(lbl_hex_pc, pos=(4, 1))
        grid_bag_sizer.Add(txt_register_pc_hex, pos=(4, 2))
        grid_bag_sizer.Add(lbl_bin_pc, pos=(4, 3))
        grid_bag_sizer.Add(txt_register_pc_bin, pos=(4, 4))

        grid_bag_sizer.Add(lbl_register_sw, pos=(5, 0), )
        grid_bag_sizer.Add(lbl_hex_sw, pos=(5, 1))
        grid_bag_sizer.Add(txt_register_sw_hex, pos=(5, 2))
        grid_bag_sizer.Add(lbl_bin_sw, pos=(5, 3))
        grid_bag_sizer.Add(txt_register_sw_bin, pos=(5, 4))

        grid_bag_sizer.Add(execution_control_panel, flag=wx.EXPAND | wx.ALIGN_CENTER, pos=(6, 0), span=(0, 5))

        # STATIC BOX
        instruction_register_box = wx.StaticBox(self, label="Instruction and Registers")
        static_box_sizer = wx.StaticBoxSizer(instruction_register_box, wx.VERTICAL)

        static_box_sizer.Add(grid_bag_sizer, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        self.SetSizer(static_box_sizer)