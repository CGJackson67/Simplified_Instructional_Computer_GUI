import wx

from SIC_GUI.Simulator.control_panel import ControlPanel
from SIC_GUI.Simulator.load_status_panel import LoadStatusPanel
from SIC_GUI.Simulator.peripheral_panel import PeripheralsPanel
from SIC_GUI.Simulator.run_program_panel import RunProgramPanel


class SimulatorPanel(wx.Panel):
    def __init__(self, parent):
        super(SimulatorPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROL PANEL
        control_panel = ControlPanel(self)

        # NOTEBOOK
        notebook_simulator = wx.Notebook(self)

        tab_simulator_status = LoadStatusPanel(notebook_simulator)
        notebook_simulator.AddPage(tab_simulator_status, "Load Status")

        tab_run_program = RunProgramPanel(notebook_simulator)
        notebook_simulator.AddPage(tab_run_program, "Run Program")

        tab_peripherals = PeripheralsPanel(notebook_simulator)
        notebook_simulator.AddPage(tab_peripherals, "Peripherals")

        # LAYOUT
        vertical_box_sizer.Add(control_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=20)
        vertical_box_sizer.Add(notebook_simulator, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,
                            border=20)

        self.SetSizer(vertical_box_sizer)
