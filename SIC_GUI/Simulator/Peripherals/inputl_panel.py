import wx


class InputPanel(wx.Panel):
    def __init__(self, parent):
        super(InputPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        input_grid_bag_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        # CONTROLS
        lbl_input = wx.StaticText(self, label="Input")
        txt_input = wx.TextCtrl(self)
        txt_input.SetMaxLength(1)

        # LAYOUT
        input_grid_bag_sizer.Add(lbl_input, pos=(0, 0))
        input_grid_bag_sizer.Add(txt_input, flag=wx.EXPAND, pos=(0, 1))
        input_grid_bag_sizer.AddGrowableCol(1)

        self.SetSizer(input_grid_bag_sizer)