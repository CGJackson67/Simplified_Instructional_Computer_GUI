import wx

from SIC_Simulator.sic_memory_model import MEMORY_MODEL


class RightPanel(wx.Panel):
    def __init__(self, parent):
        super(RightPanel, self).__init__(parent)

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROLS
        MONOSPACED_FONT = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.txt_memory = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.txt_memory.SetFont(MONOSPACED_FONT)

        # LAYOUT
        vertical_box_sizer.Add(self.txt_memory, proportion=1, flag=wx.EXPAND)

        # STATIC BOX
        memory_static_box = wx.StaticBox(self, label="Memory")
        static_box_sizer = wx.StaticBoxSizer(memory_static_box, wx.VERTICAL)

        static_box_sizer.Add(vertical_box_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(static_box_sizer)

    def update_memory_text_ctrl(self):
        self.txt_memory.Clear()
        self.txt_memory.WriteText(MEMORY_MODEL.dump_memory())
        self.txt_memory.ShowPosition(0)
