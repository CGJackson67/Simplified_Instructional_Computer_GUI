import wx

from SIC_GUI.Simulator.Run_Program.left_panel import LeftPanel
from SIC_GUI.Simulator.Run_Program.right_panel import RightPanel


class RunProgramPanel(wx.Panel):
    def __init__(self, parent):
        super(RunProgramPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)

        # LAYOUT
        horizontal_box_sizer.Add(self.left_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        horizontal_box_sizer.Add(self.right_panel, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=10)

        self.SetSizer(horizontal_box_sizer)

    def update_memory_text_ctrl(self):
        self.right_panel.update_memory_text_ctrl()


    def update_register_text_ctrls(self):
        self.left_panel.update_register_text_ctrls()


    def update_instruction_text_ctrl(self, line_of_code):
        self.left_panel.update_instruction_text_ctrl(line_of_code)


    def print_assembly_listing_line(self, parsed_assembly_listing_dict):
        self.left_panel.print_assembly_listing_line(parsed_assembly_listing_dict)

    def set_state_of_run_program_buttons(self, enable_reset_button, enable_run_button, enable_step_button):
        self.left_panel.set_state_of_run_program_buttons(enable_reset_button, enable_run_button, enable_step_button)

    def dump_registers(self):
        self.left_panel.dump_registers()

    def initialize_txt_instruction_and_registers_history(self):
        self.left_panel.initialize_txt_instruction_and_registers_history()