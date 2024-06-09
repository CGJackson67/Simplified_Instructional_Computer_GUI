import wx


class ExecutionControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ExecutionControlPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        self.btn_run = wx.Button(self, label="Run")
        self.btn_run.SetToolTip("Click to run program to completion")
        self.btn_step = wx.Button(self, label="Step")
        self.btn_step.SetToolTip("Click to execute one instruction at a time")
        self.btn_reset = wx.Button(self, label="Reset")
        self.btn_reset.SetToolTip("Click to reset program")

        # LAYOUT
        grid_bag_sizer.Add(self.btn_reset, pos=(0,0))
        grid_bag_sizer.Add(self.btn_run, pos=(0,1))
        grid_bag_sizer.Add(self.btn_step, pos=(0,2))

        self.SetSizer(grid_bag_sizer)

    def set_state_of_run_program_buttons(self, enable_reset_button, enable_run_button, enable_step_button):
        self.btn_reset.Enable(enable_reset_button)
        self.btn_run.Enable(enable_run_button)
        self.btn_step.Enable(enable_step_button)