import os
import wx

from SIC_GUI.Simulator.Peripherals.input_device_f1_dialog import InputDeviceF1Dialog
from SIC_GUI.Simulator.Peripherals.output_device_05_dialog import OutputDevice05Dialog
from SIC_GUI.Simulator.control_panel import ControlPanel
from SIC_GUI.Simulator.load_status_panel import LoadStatusPanel
from SIC_GUI.Simulator.run_program_panel import RunProgramPanel
from SIC_Peripherals.sic_output_device_05 import initialize_output_device_05
from SIC_Simulator.sic_assembly_listing_parser import sic_assembly_listing_parser, SICAssemblyListingParserError
from SIC_Simulator.sic_loader import load_program_object_code
from SIC_Simulator.sic_memory_model import MEMORY_MODEL
from SIC_Simulator.sic_object_code_parser import sic_object_code_parser, SICObjectCodeParserError
from SIC_Simulator.sic_operation_executor import execute_operation
from SIC_Simulator.sic_register_model import SICRegisterContentsError, initialize_registers, REGISTER_DICT, REGISTER_PC
from SIC_Utilities.sic_messaging import print_error


class SimulatorPanel(wx.Panel):
    def __init__(self, parent):
        super(SimulatorPanel, self).__init__(parent)

        self.parsed_object_code_dict_list = None
        self.parsed_assembly_listing_dict = None
        self.program_start_address = None

        self.SetBackgroundColour("light gray")

        self.enable_run_program_tab = False

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROL PANEL
        self.control_panel = ControlPanel(self)

        # NOTEBOOK
        self.notebook_simulator = wx.Notebook(self)

        self.tab_load_status = LoadStatusPanel(self.notebook_simulator)
        self.notebook_simulator.AddPage(self.tab_load_status, "Load Status")

        self.tab_run_program = RunProgramPanel(self.notebook_simulator)
        self.notebook_simulator.AddPage(self.tab_run_program, "Run Program")

        # LAYOUT
        vertical_box_sizer.Add(self.control_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=20)
        vertical_box_sizer.Add(self.notebook_simulator, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,
                               border=20)

        self.SetSizer(vertical_box_sizer)

        # EVENT HANDLING
        self.Bind(wx.EVT_BUTTON, self.button_handler)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.file_picker_change_handler)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.notebook_tab_handler)

    def file_picker_change_handler(self, event):
        # Get the file path from the file picker
        object_code_file_path = self.control_panel.get_file_path()

        # Verify associated assembly listing file exists
        assembly_listing_file_path = object_code_file_path.replace(".obj", ".lst")

        if not os.path.exists(assembly_listing_file_path):
            wx.MessageBox("Assembly listing file for this object code file not found",
                          "Associated Assembly Listing File Not Found",
                          wx.OK | wx.ICON_ERROR)
            return

        # Load the file into assembler status text control
        # Add ready message to assembler status text control
        self.tab_load_status.load_object_code_file(object_code_file_path)

        # Enable the Load button
        self.control_panel.enable_load_button()

        # Select the status tab
        self.notebook_simulator.ChangeSelection(0)

    def notebook_tab_handler(self, event):
        tab = event.GetEventObject()
        tab_number = tab.GetSelection()
        if tab.GetPageText(tab_number) == "Load Status":
            if not self.enable_run_program_tab:
                event.Veto()

    def button_handler(self, event):
        button_label = event.GetEventObject().GetLabel()

        match button_label:
            case "Load":
                self.load_button_handler()
            case "Reset":
                self.reset_button_handler()
            case "Run":
                self.run_button_handler()
            case "Step":
                self.step_button_handler()

    def load_button_handler(self):
        try:
            # Open object code file
            object_code_file_path = self.control_panel.get_file_path()
            object_code_file = open(object_code_file_path, "rt")

            # Open assembly listing file
            assembly_listing_file_path = object_code_file_path.replace(".obj", ".lst")
            assembly_listing_file = open(assembly_listing_file_path, "rt")

            # Parse object code and assembly listing files
            self.parsed_object_code_dict_list = sic_object_code_parser(object_code_file)
            self.parsed_assembly_listing_dict = sic_assembly_listing_parser(assembly_listing_file)

            # Initialize registers and set the program counter
            initialize_registers()
            header_record_dict = self.parsed_object_code_dict_list[0]
            self.program_start_address = header_record_dict["program_start_address"]
            REGISTER_DICT[REGISTER_PC].set_hex_string(self.program_start_address)

            # Initialize memory and load object code into memory
            load_program_object_code(self.parsed_object_code_dict_list)
            self.tab_run_program.update_memory_text_ctrl(self.program_start_address)
            self.tab_load_status.set_load_status("Object code program loaded into memory\n")

            self.tab_run_program.update_register_text_ctrls()
            self.tab_load_status.set_load_status("Registers initialized\n")

            # Initialize Output Device 05
            initialize_output_device_05()

            # Display first instruction
            self.tab_run_program.update_instruction_text_ctrl(
                self.parsed_assembly_listing_dict[self.program_start_address.rjust(6, "0")])

            # Initialize instruction and register history
            self.tab_run_program.initialize_txt_instruction_and_registers_history()

            # Enable run program buttons
            self.tab_run_program.set_state_of_run_program_buttons(enable_reset_button=True, enable_run_button=True,
                                                                  enable_step_button=True)

            # Enable run program tabs
            self.enable_run_program_tab = True

            # Status as ready to run
            dialog_response = wx.MessageDialog(self, message="Click OK to go to the Run Program tab",
                                               caption="Program Loaded and Ready to Run",
                                               style=wx.OK | wx.ICON_INFORMATION)

            if dialog_response.ShowModal() == wx.ID_OK:
                self.notebook_simulator.ChangeSelection(1)

        except (SICObjectCodeParserError, SICAssemblyListingParserError, SICRegisterContentsError) as ex:
            print_error(str(ex))
            self.tab_load_status.set_load_status(str(ex), True)

    def run_button_handler(self):
        continue_execution = True

        while continue_execution:
            # Update Instruction and Registers History and Memory
            self.tab_run_program.print_assembly_listing_line(self.parsed_assembly_listing_dict)
            continue_execution = execute_operation(REGISTER_DICT, MEMORY_MODEL, self)
            self.tab_run_program.dump_registers()

            # Update Instruction and Registers
            self.tab_run_program.update_instruction_text_ctrl(
                self.parsed_assembly_listing_dict[REGISTER_DICT[REGISTER_PC].get_hex_string()])
            self.tab_run_program.update_register_text_ctrls()

            self.tab_run_program.update_memory_text_ctrl(REGISTER_DICT[REGISTER_PC].get_hex_string())

    def step_button_handler(self):
        # Update Instruction and Registers History and Memory
        self.tab_run_program.print_assembly_listing_line(self.parsed_assembly_listing_dict)
        execute_operation(REGISTER_DICT, MEMORY_MODEL, self)
        self.tab_run_program.dump_registers()
        self.tab_run_program.update_memory_text_ctrl(REGISTER_DICT[REGISTER_PC].get_hex_string())

        # Update Instruction and Registers
        self.tab_run_program.update_instruction_text_ctrl(
            self.parsed_assembly_listing_dict[REGISTER_DICT[REGISTER_PC].get_hex_string()])
        self.tab_run_program.update_register_text_ctrls()

    def reset_button_handler(self):
        # Initialize registers and set the program counter
        initialize_registers()
        header_record_dict = self.parsed_object_code_dict_list[0]
        self.program_start_address = header_record_dict["program_start_address"]
        REGISTER_DICT[REGISTER_PC].set_hex_string(self.program_start_address)

        # Initialize memory and load object code into memory
        load_program_object_code(self.parsed_object_code_dict_list)
        self.tab_run_program.update_memory_text_ctrl(self.program_start_address)

        self.tab_run_program.update_register_text_ctrls()

        # Display first instruction
        self.tab_run_program.update_instruction_text_ctrl(
            self.parsed_assembly_listing_dict[self.program_start_address.rjust(6, "0")])

        # Initialize instruction and register history
        self.tab_run_program.initialize_txt_instruction_and_registers_history()

        # Initialize Output Device 05
        initialize_output_device_05()

        # Enable run program buttons
        self.tab_run_program.set_state_of_run_program_buttons(enable_reset_button=True, enable_run_button=True,
                                                              enable_step_button=True)

        # Disable Input Peripherals

        # Enable run program and peripherals tabs
        self.enable_run_program_tab = True

        # Status as ready to run
        wx.MessageBox(message="Loaded program has been reset",
                      caption="Program Reset and Ready to Run",
                      style=wx.OK | wx.ICON_INFORMATION)

    def display_error_dialog(self, error_message):
        wx.MessageBox(message=error_message,
                      caption="Program Execution Error",
                      style=wx.OK | wx.ICON_ERROR)

        self.tab_run_program.set_state_of_run_program_buttons(enable_reset_button=True, enable_run_button=False,
                                                              enable_step_button=False)

    def display_status_dialog(self, status_message):
        wx.MessageBox(message=status_message,
                      caption="Program Execution Completion",
                      style=wx.OK | wx.ICON_INFORMATION)

        self.tab_run_program.set_state_of_run_program_buttons(enable_reset_button=True, enable_run_button=False,
                                                              enable_step_button=False)

    def read_byte_input_device_F1(self, is_in_EOF_state):
        input_device_dialog = InputDeviceF1Dialog(self, "Input Device F1", is_in_EOF_state)
        response = input_device_dialog.ShowModal()
        if response == wx.ID_OK:
            input_string = input_device_dialog.read_device_input
            input_device_dialog.Destroy()
            return input_string

    def write_byte_output_device_05(self, OUTPUT_DEVICE_05_INTERFACE):
        output_device_dialog = OutputDevice05Dialog(self, "Output Device 05", OUTPUT_DEVICE_05_INTERFACE)
        response = output_device_dialog.ShowModal()
        output_device_dialog.Destroy()
