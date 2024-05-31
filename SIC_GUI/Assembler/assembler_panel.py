import wx

from SIC_GUI.Assembler.assembly_listing_panel import AssemblyListingPanel
from SIC_GUI.Assembler.assembly_status_panel import AssemblyStatusPanel
from SIC_GUI.Assembler.control_panel import ControlPanel
from SIC_GUI.Assembler.object_code_panel import ObjectCodePanel


class AssemblerPanel(wx.Panel):
    def __init__(self, parent):
        super(AssemblerPanel, self).__init__(parent)

        self.disable_file_context_tabs = False

        self.SetBackgroundColour("light gray")

        # SIZER
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # CONTROL PANEL
        control_panel = ControlPanel(self)

        # NOTEBOOK
        notebook_assembler = wx.Notebook(self)

        tab_assembler_status = AssemblyStatusPanel(notebook_assembler)
        notebook_assembler.AddPage(tab_assembler_status, "Assembly Status")

        tab_assembly_listing = AssemblyListingPanel(notebook_assembler)
        notebook_assembler.AddPage(tab_assembly_listing, "Assembly Listing")

        tab_object_code = ObjectCodePanel(notebook_assembler)
        notebook_assembler.AddPage(tab_object_code, "Object Code")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.notebook_tab_handler)

        # LAYOUT
        vertical_box_sizer.Add(control_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=20)
        vertical_box_sizer.Add(notebook_assembler, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,
                               border=20)

        self.SetSizer(vertical_box_sizer)

    def notebook_tab_handler(self, event):
        tab = event.GetEventObject()
        tab_number = tab.GetSelection()
        if tab.GetPageText(tab_number) == "Assembly Status":
            if self.disable_file_context_tabs:
                event.Veto()
