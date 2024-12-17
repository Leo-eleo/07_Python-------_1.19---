# -*- coding: utf-8 -*-
import sys

import wx
import wx.xrc
import win32com.client as win32

import images


def _exit_sys(event):
    stone = wx.MessageDialog(None, 'アプリを終了しますか？／Do you want to exit the application?', ' ',
                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
    if stone.ShowModal() == wx.ID_YES:
        stone.Destroy()
        sys.exit()


def on_outlook_click(event):
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.To = "ToolTeam@accenture.com"
    mail.Subject = ""
    mail.HtmlBody = ""
    mail.Display(True)


def _get_logo():
    logo = wx.Icon()
    logo.CopyFromBitmap(getattr(images, "logo").GetBitmap())
    return logo


class MemberSplitFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞メンバー分割／Asset Analysis Support>Asset Analysis>Member Split", pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        self.GetMenuBar()
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"入力フォルダ\nInput Folder", style=wx.ALIGN_LEFT) 
        m_st_out = wx.StaticText(m_panel, label=u"出力フォルダ\nOutput Folder", style=wx.ALIGN_LEFT) 

        # Picker(ファイル選択)
        m_dp_input = wx.DirPickerCtrl(m_panel, message=u"入力フォルダを選択ください／Please select an input folder",
                                      style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_dp_input.SetLabel(u"入力フォルダ／Input Folder") 
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_dp_out.SetLabel(u"出力フォルダ／Output Folder") 

        # 実行ボタン
        m_b_jcl_out = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT) 

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_input, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_input, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl_out, 1, flag=wx.ALIGN_CENTER, border=10)

        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_dp_input = m_dp_input
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class JclOutFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞JCL呼出ありカタプロ一覧作成／Asset Analysis Support>Asset Analysis>Generate a List of PROC with JCL Calls", pos=wx.DefaultPosition,
                          size=wx.Size(800, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        self.GetMenuBar()
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_excel_out = wx.StaticText(m_panel, label=u"解析済みExcel出力フォルダ\nAnalyzed Excel Output Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_excel_out = wx.DirPickerCtrl(m_panel, message=u"解析済みExcelフォルダを選択ください／Please select an analyzed Excel folder",
                                          style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_excel_out.SetLabel(u"解析済みExcel出力フォルダ／Analyzed Excel Output Folder")

        # 実行ボタン
        m_b_jcl_out = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_excel_out, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_excel_out, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl_out, 1, flag=wx.ALIGN_CENTER, border=10)

        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_excel_out = m_dp_excel_out

        # Connect Events
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class CobolFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞PGM解析＞COBOL解析／Asset Analysis Support>PGM Analysis>COBOL Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT) 
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT) 
        m_st_cobol = wx.StaticText(m_panel, label=u"COBOLパス\nCOBOL Path", style=wx.ALIGN_LEFT) 
        m_st_db_out = wx.StaticText(m_panel, label=u"解析済みDB出力フォルダ\nAnalyzed DB Output Folder", style=wx.ALIGN_LEFT) 

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB") 
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File") 
        m_dp_cobol = wx.DirPickerCtrl(m_panel, message=u"COBOL資源フォルダを選択ください／Please select a COBOL resource folder",
                                      style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_dp_cobol.SetLabel(u"COBOLパス／COBOL Path") 

        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"解析済みExcelフォルダを選択ください／Please select an analyzed Excel folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_dp_db_out.SetLabel(u"解析済みExcel出力フォルダ／Analyzed Excel Output Folder") 

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT) 

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_cobol, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_cobol, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_cobol, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(5, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_cobol = m_dp_cobol
        self.m_dp_db_out = m_dp_db_out

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_cobol_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_cobol_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class NaturalFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞PGM解析＞Natural解析／Asset Analysis Support>PGM Analysis>Natural Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_natrual = wx.StaticText(m_panel, label=u"Naturalパス\nNatural Path", style=wx.ALIGN_LEFT)
        m_st_db_out = wx.StaticText(m_panel, label=u"解析済みDB出力フォルダ\nAnalyzed DB Output Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_natrual = wx.DirPickerCtrl(m_panel, message=u"Natural資源フォルダを選択ください／Please select a Natural resource folder",
                                        style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_natrual.SetLabel(u"Naturalパス／Natural Path")

        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"解析済みDBフォルダを選択ください／Please select an analyzed DB folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_db_out.SetLabel(u"解析済みDB出力フォルダ／Analyzed DB Output Folder")

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_natrual, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_natrual, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_cobol, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(5, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_natrual = m_dp_natrual
        self.m_dp_db_out = m_dp_db_out

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_natrual_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_natrual_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()



class ClistFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞PGM解析＞Clist解析／Asset Analysis Support>Asset Analysis>PGM Analysis>Clist Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_clist = wx.StaticText(m_panel, label=u"Clistパス\nClist Path", style=wx.ALIGN_LEFT)
        m_st_db_out = wx.StaticText(m_panel, label=u"解析済みDB出力フォルダ\nAnalyzed DB Output Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_clist = wx.DirPickerCtrl(m_panel, message=u"Clist資源フォルダを選択ください／Please select a Clist resource folder",
                                        style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_clist.SetLabel(u"Clistパス／Clist Path")

        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"解析済みDBフォルダを選択ください／Please select an analyzed DB folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_db_out.SetLabel(u"解析済みDB出力フォルダ／Analyzed DB Output Folder")

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_clist, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_clist, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_cobol, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(5, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_clist = m_dp_clist
        self.m_dp_db_out = m_dp_db_out

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_clist_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_clist_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class CParseFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞PGM解析＞C言語解析／Asset Analysis Support>Asset Analysis>PGM Analysis>C Language Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 460), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_c_parse = wx.StaticText(m_panel, label=u"Cパス\nC Language Path", style=wx.ALIGN_LEFT)
        m_st_db_out = wx.StaticText(m_panel, label=u"解析済みDB出力フォルダ\nAnalyzed DB Output Folder", style=wx.ALIGN_LEFT)
        m_st_rm_72_80 = wx.StaticText(m_panel, label=u"ビット72～80を削除\nDelete bits from 72 to 80", style=wx.ALIGN_LEFT)

        # チェックボックス
        m_cb_is_rm_72_80 = wx.CheckBox(m_panel)
        m_cb_is_rm_72_80.SetValue(False)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_c_parse = wx.DirPickerCtrl(m_panel, message=u"C資源フォルダを選択ください／Please select a C Language resource folder",
                                        style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_c_parse.SetLabel(u"Cパス／C Language Path")

        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"解析済みDBフォルダを選択ください／Please select an analyzed DB folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_db_out.SetLabel(u"解析済みDB出力フォルダ／Analyzed DB Output Folder")

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_c_parse, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_c_parse, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_rm_72_80, pos=(5, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_cb_is_rm_72_80, pos=(5, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_cb_is_rm_72_80 = m_cb_is_rm_72_80

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_cobol, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(6, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_c_parse = m_dp_c_parse
        self.m_dp_db_out = m_dp_db_out

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_c_parse_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_c_parse_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()




class NativePliFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞PGM解析＞PLI解析＞NativePLIソース整形／Asset Analysis Support>PGM Analysis>PLI Analysis>NativePLI Source Formatting",
                          pos=wx.DefaultPosition,
                          size=wx.Size(850, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        self.GetMenuBar()
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"入力フォルダ\nInput Folder", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"出力フォルダ\nOutput Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_dp_input = wx.DirPickerCtrl(m_panel, message=u"入力フォルダを選択ください／Please select an input folder",
                                      style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_input.SetLabel(u"入力フォルダ／Input Folder")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"出力フォルダ／Output Folder")

        # 実行ボタン
        m_b_jcl_out = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_input, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_input, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl_out, 1, flag=wx.ALIGN_CENTER, border=10)

        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_dp_input = m_dp_input
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class RationalizationFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞PGM解析＞PLI解析＞PLIソース解析／Asset Analysis Support>PGM Analysis>PLI Analysis>PLI Source Code Analysis",
                          pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_pli = wx.StaticText(m_panel, label=u"PLIパス\nPLI Path", style=wx.ALIGN_LEFT)
        m_st_db_out = wx.StaticText(m_panel, label=u"解析済みDB出力フォルダ\nAnalyzed DB Output Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_pli = wx.DirPickerCtrl(m_panel, message=u"PLI資源フォルダを選択ください／Please select a PLI resource folder",
                                        style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_pli.SetLabel(u"PLIパス／PLI Path")

        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"解析済みDBフォルダを選択ください／Please select an analyzed DB folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_db_out.SetLabel(u"解析済みDB出力フォルダ／Analyzed DB Output Folder")

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_pli, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_pli, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_cobol, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(5, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_pli = m_dp_pli
        self.m_dp_db_out = m_dp_db_out

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_pli_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_pli_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class PliCmdFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞PGM解析＞PLI解析＞呼ぶ関係抽出／Asset Analysis Support>PGM Analysis>PLI Analysis>Call Relationship Extraction",
                          pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        self.GetMenuBar()
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"入力ファイル\nInput File", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"出力フォルダ\nOutput Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_input = wx.FilePickerCtrl(m_panel, message=u"入力フォルダを選択ください／Please select an input folder", wildcard=u"*.xlsx;*.xlsm",
                                       style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_input.SetLabel(u"出力用ファイル／File for Output")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"出力フォルダ／Output Folder")

        # 実行ボタン
        m_b_jcl_out = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_input, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_input, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl_out, 1, flag=wx.ALIGN_CENTER, border=10)

        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_input = m_fp_input
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class PliFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞PGM解析＞PLI解析／Asset Analysis Support>PGM Analysis>PLI Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(600, 460), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_native = wx.Button(m_panel, label=u"NativePLIソース整形\nNativePLI Source Formatting", style=wx.BU_EXACTFIT)
        # m_b_pli = wx.Button(m_panel, label=u"PLI論理化ソース生成\nPLI Logical Source Code Generation", style=wx.BU_EXACTFIT)
        m_b_rationalization = wx.Button(m_panel, label=u"PLIソース解析\nPLI Source Code Analysis", style=wx.BU_EXACTFIT)
        m_b_relationship = wx.Button(m_panel, label=u"呼ぶ関係抽出\nCall Relationship Extraction", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_native, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        # m_gb_sizer.Add(m_b_pli, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_rationalization, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_relationship, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_native.Bind(wx.EVT_BUTTON, self.on_native_click)
        # m_b_pli.Bind(wx.EVT_BUTTON, self.on_pli_click)
        m_b_rationalization.Bind(wx.EVT_BUTTON, self.on_rationalization_click)
        m_b_relationship.Bind(wx.EVT_BUTTON, self.on_relationship_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_native_click(self, event):
        event.Skip()

    # def on_pli_click(self, event):
    #     event.Skip()

    def on_rationalization_click(self, event):
        event.Skip()

    def on_relationship_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class PgmFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞PGM解析／Asset Analysis Support>PGM Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(460, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_cobol = wx.Button(m_panel, label=u"COBOL解析\nCOBOL Analysis", style=wx.BU_EXACTFIT) 
        m_b_pli = wx.Button(m_panel, label=u"PLI解析\nPLI Analysis", style=wx.BU_EXACTFIT) 
        m_b_natural = wx.Button(m_panel, label=u"Natural解析\nNatural Analysis", style=wx.BU_EXACTFIT) 
        m_b_clist = wx.Button(m_panel, label=u"Clist解析\nClist Analysis", style=wx.BU_EXACTFIT) 
        m_b_c_parse = wx.Button(m_panel, label=u"C言語解析\nC Language Analysis", style=wx.BU_EXACTFIT) 

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_cobol, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_pli, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_natural, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_clist, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_c_parse, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=15)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_cobol.Bind(wx.EVT_BUTTON, self.on_cobol_click)
        m_b_pli.Bind(wx.EVT_BUTTON, self.on_pli_click)
        m_b_natural.Bind(wx.EVT_BUTTON, self.on_natural_click)
        m_b_clist.Bind(wx.EVT_BUTTON, self.on_clist_click)
        m_b_c_parse.Bind(wx.EVT_BUTTON, self.on_c_parse_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_cobol_click(self, event):
        event.Skip()

    def on_pli_click(self, event):
        event.Skip()

    def on_natural_click(self, event):
        event.Skip()

    def on_clist_click(self, event):
        event.Skip()

    def on_c_parse_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class SysinFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞外部SYSIN取り込み／Asset Analysis Support>Asset Analysis>External SYSIN Import", pos=wx.DefaultPosition,
                          size=wx.Size(800, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_sysin = wx.StaticText(m_panel, label=u"SYSINパス\nJCL Parameter Path", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_sysin = wx.DirPickerCtrl(m_panel, message=u"SYSIN資源フォルダを選択ください／Please select a SYSIN resource folder",
                                      style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_sysin.SetLabel(u"SYSINパス／JCL Parameter Path")

        # 実行ボタン
        m_b_sysin = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)
        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_sysin, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_sysin, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_sysin, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_sysin = m_dp_sysin

        # Connect Events
        m_b_sysin.Bind(wx.EVT_BUTTON, self.on_sysin_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_sysin_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class ProcFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞PROC解析／Asset Analysis Support>Asset Analysis>PROC Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_proc = wx.StaticText(m_panel, label=u"カタプロパス\nPROC Path", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_proc = wx.DirPickerCtrl(m_panel, message=u"カタプロ資源フォルダを選択ください／Please select a PROC resource folder",
                                     style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_proc.SetLabel(u"カタプロパス／PROC Path")

        # 実行ボタン
        m_b_proc = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_proc, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_proc, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_proc, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_proc = m_dp_proc

        # Connect Events
        m_b_proc.Bind(wx.EVT_BUTTON, self.on_proc_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_proc_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class JclFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞JCL解析／Asset Analysis Support>Asset Analysis>JCL Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"言語解析DB\nLanguage Analysis DB", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_jcl = wx.StaticText(m_panel, label=u"JCL格納パス\nJCL Storage Path", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_analysis_db = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_analysis_db.SetLabel(u"言語解析DB／Language Analysis DB")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_jcl = wx.DirPickerCtrl(m_panel, message=u"JCL資源フォルダを選択ください／Please select a JCL resource folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_jcl.SetLabel(u"JCL格納パス／JCL Storage Path")

        m_b_jcl = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_analysis_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting_file, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_jcl, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_jcl, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_analysis_db = m_fp_analysis_db
        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_jcl = m_dp_jcl

        # Connect Events
        m_b_jcl.Bind(wx.EVT_BUTTON, self.on_jcl_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class GrepFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析＞Grep検索／Asset Analysis Support>Asset Analysis>Grep Search", pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(self, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイルパス\nSetup File Path", style=wx.ALIGN_LEFT)
        m_st_output = wx.StaticText(m_panel, label=u"出力用ファイル\nFile for Output", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file path", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイルパス／Setup File Path")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"出力フォルダ／Output Folder")
        # 実行ボタン
        m_b_Result = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL, border=10)
        m_gb_sizer.Add(m_panel, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL)
        m_gb_sizer.AddGrowableCol(2)

        m_panel_gb_sizer.Add(m_st_setting_file, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_setting_file, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_output, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_dp_out, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_Result, 1, flag=wx.ALIGN_CENTER, border=10)
        m_panel_gb_sizer.Add(vbox, pos=(2, 0), span=(2, 4), flag=wx.EXPAND | wx.ALL)

        m_panel_gb_sizer.AddGrowableCol(3)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        self.SetSizer(m_gb_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_Result.Bind(wx.EVT_BUTTON, self.on_result_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_result_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class AnalysisFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析／Asset Analysis Support>Asset Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(460, 700), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_member_spilt = wx.Button(m_panel, label=u"メンバー分割\nMember Split", style=wx.BU_EXACTFIT) 
        m_b_jcl = wx.Button(m_panel, label=u"JCL解析\nJCL Analysis", style=wx.BU_EXACTFIT) 
        m_b_proc = wx.Button(m_panel, label=u"PROC解析\nPROC Analysis", style=wx.BU_EXACTFIT) 
        m_b_sysin = wx.Button(m_panel, label=u"外部SYSIN取り込み\nExternal SYSIN Import", style=wx.BU_EXACTFIT) 
        m_b_pgm = wx.Button(m_panel, label=u"PGM解析\nPGM Analysis", style=wx.BU_EXACTFIT) 
        m_b_jcl_out = wx.Button(m_panel, label=u"JCL呼出ありカタプロ一覧作成\nGenerate a List of PROC with JCL Calls", style=wx.BU_EXACTFIT) 
        m_b_grep = wx.Button(m_panel, label=u"Grep検索\nGrep Search", style=wx.BU_EXACTFIT) 

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_member_spilt, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_jcl, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_proc, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_sysin, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_pgm, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_jcl_out, pos=(6, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_grep, pos=(7, 0), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_jcl.Bind(wx.EVT_BUTTON, self.on_jcl_analysis_click)
        m_b_proc.Bind(wx.EVT_BUTTON, self.on_proc_analysis_click)
        m_b_sysin.Bind(wx.EVT_BUTTON, self.on_sysin_analysis_click)
        m_b_pgm.Bind(wx.EVT_BUTTON, self.on_pgm_analysis_click)
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_b_member_spilt.Bind(wx.EVT_BUTTON, self.on_member_spilt_click)
        m_b_grep.Bind(wx.EVT_BUTTON, self.on_grep_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_analysis_click(self, event):
        event.Skip()

    def on_proc_analysis_click(self, event):
        event.Skip()

    def on_sysin_analysis_click(self, event):
        event.Skip()

    def on_pgm_analysis_click(self, event):
        event.Skip()

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_member_spilt_click(self, event):
        event.Skip()

    def on_grep_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class RelevanceAnalysisFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞関連性解析＞個別関連性解析／Asset Analysis Support>Relationship Analysis>Individual Relationship Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"個別関連性出力先フォルダ\nOutput Folder for Individual Relationship", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイル／Setup File")
        m_dp_jcl = wx.DirPickerCtrl(m_panel, message=u"個別関連性出力先フォルダを選択ください／Please select an output folder for individual relationship",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)
        m_dp_jcl.SetLabel(u"出力先フォルダ／Output Folder")

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_setting_file, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting_file, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_jcl, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_setting_file = m_fp_setting_file
        self.m_dp_jcl = m_dp_jcl

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class RelevanceMajiFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞関連性解析＞個別関連性マージ／Asset Analysis Support>Relationship Analysis>Individual Relationship Merging", pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_analysis_db = wx.StaticText(m_panel, label=u"個別関連性出力済みフォルダ\nIndividual Relationship Output Folder", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"関連性マージ版出力先フォルダ\nOutput Folder for The Relationship Merged Document", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_out = wx.DirPickerCtrl(m_panel, message=u"個別関連性出力済みフォルダを選択ください／Please select an individual relationship output folder",
                                    style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_out.SetLabel(u"個別関連性出力済みフォルダ／Individual Relationship Output Folder")
        m_dp_jcl = wx.DirPickerCtrl(m_panel, message=u"関連性マージ版出力先フォルダを選択ください／Please select an output folder for the relationship merged version",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_jcl.SetLabel(u"関連性マージ版出力先フォルダ／Output Folder for The Relationship Merged Version")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_analysis_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_out, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_jcl, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_out = m_fp_out
        self.m_dp_jcl = m_dp_jcl

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class RelevanceCompareFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞関連性解析＞関連性マージ差分出力／Asset Analysis Support > Relationship Analysis > Relationship Merged Document Diff Output", pos=wx.DefaultPosition,
                          size=wx.Size(900, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_new = wx.StaticText(m_panel, label=u"新規関連性マージ版\nNew Relationship Merged Document", style=wx.ALIGN_LEFT)
        m_st_old = wx.StaticText(m_panel, label=u"旧関連性マージ版\nOld Relationship Merged Document", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"関連性差分出力先フォルダ\nRelationship Document Diff Output Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_new = wx.FilePickerCtrl(m_panel, message=u"新規関連性マージ版フォルダを選択ください／Please select a new relationship merged version", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_new.SetLabel(u"新規関連性マージ版／New Relationship Merged Document")
        m_fp_old = wx.FilePickerCtrl(m_panel, message=u"旧関連性マージ版フォルダを選択ください／Please select an old relationship merged version", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_old.SetLabel(u"旧関連性マージ版／Old Relationship Merged Document")
        m_dp_jcl = wx.DirPickerCtrl(m_panel, message=u"関連性差分出力先フォルダを選択ください／Please select an output folder for relationship diff",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_jcl.SetLabel(u"関連性差分出力先フォルダ／Relationship Document Diff Output Folder")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_new, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_new, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_old, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_old, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_jcl, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_new = m_fp_new
        self.m_fp_old = m_fp_old
        self.m_dp_jcl = m_dp_jcl

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class RelevanceFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞関連性解析／Asset Analysis Support>Relationship Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(650, 460), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_analysis = wx.Button(m_panel, label=u"個別関連性解析\nIndividual Relationship Analysis", style=wx.BU_EXACTFIT)
        m_b_maji = wx.Button(m_panel, label=u"個別関連性マージ\nIndividual Relationship Merging", style=wx.BU_EXACTFIT)
        m_b_compare = wx.Button(m_panel, label=u"関連性マージ差分出力\nRelationship Document Diff Output", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_analysis, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_maji, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_compare, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_b_maji.Bind(wx.EVT_BUTTON, self.on_maji_click)
        m_b_compare.Bind(wx.EVT_BUTTON, self.on_compare_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_maji_click(self, event):
        event.Skip()

    def on_compare_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート／Asset Analysis Support", pos=wx.DefaultPosition,
                          size=wx.Size(460, 540), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_b_sizer = wx.BoxSizer(wx.VERTICAL)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)

        # 文言
        m_st1 = wx.StaticText(m_panel, label=u"※エラーが発生する場合、ツールチーム(ToolTeam@accenture.com)にご連絡ください。\nIf any errors occur, please contact the Tool Team (ToolTeam@accenture.com).", 
                            style=wx.ALIGN_LEFT)
        m_st1.SetFont(wx.Font(7, 75, 90, 90, False, "Meiryo"))
        m_st1.SetForegroundColour(wx.Colour(255, 0, 0))
        m_st1.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        m_st1.SetToolTip("こちらをクリックしてください／Click here") # ツールチップの設定

        # 実行ボタン
        m_b_class_asset = wx.Button(m_panel, label=u"資産分類\nAssets Classification", style=wx.BU_EXACTFIT) 
        m_b_analysis_asset = wx.Button(m_panel, label=u"資産解析\nAsset Analysis", style=wx.BU_EXACTFIT) 
        m_b_relevance = wx.Button(m_panel, label=u"関連性解析\nRelationship Analysis", style=wx.BU_EXACTFIT) 
        # m_b_start = wx.Button(m_panel, label=u"起点解析\nStarting Point Analysis", style=wx.BU_EXACTFIT) # Starting Point Analysisボタンを非表示にする
        m_b_arrange_data = wx.Button(m_panel, label=u"顧客データ整理\nOrganize Client Data", style=wx.BU_EXACTFIT) 
        m_b_machine_result = wx.Button(m_panel, label=u"資産解析結果加工\nProcessing of Asset Analysis Results", style=wx.BU_EXACTFIT) 
        

        m_panel_gb_sizer.Add(m_b_class_asset, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_panel_gb_sizer.Add(m_b_analysis_asset, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_panel_gb_sizer.Add(m_b_relevance, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        # m_panel_gb_sizer.Add(m_b_start, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15) # Starting Point Analysisボタンを非表示にする
        m_panel_gb_sizer.Add(m_b_machine_result, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_panel_gb_sizer.Add(m_b_arrange_data, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_panel_gb_sizer.Add(m_st1, pos=(5, 0), flag=wx.ALL)
        m_panel_gb_sizer.AddGrowableCol(0)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        m_b_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(m_b_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_class_asset.Bind(wx.EVT_BUTTON, self.on_class_asset_click)
        m_b_analysis_asset.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_b_relevance.Bind(wx.EVT_BUTTON, self.on_relevance_click)
        # m_b_start.Bind(wx.EVT_BUTTON, self.on_start_click) # Starting Point Analysisボタンを非表示にする
        m_b_arrange_data.Bind(wx.EVT_BUTTON, self.on_arrange_data_click)
        m_b_machine_result.Bind(wx.EVT_BUTTON, self.on_machine_result_click)
        m_st1.Bind(wx.EVT_LEFT_DOWN, on_outlook_click) 
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_class_asset_click(self, event):
        event.Skip()

    def on_analysis_click(self, event):
        event.Skip()

    def on_relevance_click(self, event):
        event.Skip()

    def on_start_click(self, event):
        event.Skip()

    def on_arrange_data_click(self, event):
        event.Skip()

    def on_machine_result_click(self, event):
        event.Skip()


class ClassAssetFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産分類／Asset Analysis Support>Assets Classification", pos=wx.DefaultPosition, 
                          size=wx.Size(800, 820), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_gb_sizer = wx.GridBagSizer(10, 0)
        self.m_gb_sizer = m_gb_sizer

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        self.m_panel = m_panel

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)
        self.m_panel_gb_sizer = m_panel_gb_sizer

        # 戻るボタン
        m_bb_back = wx.BitmapButton(self, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"資産入力フォルダ\nAsset Input Folder", style=wx.ALIGN_LEFT) 
        m_st_output = wx.StaticText(m_panel, label=u"結果出力フォルダ\nResult Output Folder", style=wx.ALIGN_LEFT) 
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイルパス\nSetup File Path", style=wx.ALIGN_LEFT) 
        m_st_db_boll = wx.StaticText(m_panel, label=u"実行前に関連TABLEクリアする\nClear related TABLE before execution", style=wx.ALIGN_LEFT) 
        m_st_db_path = wx.StaticText(m_panel, label=u"DBパス\nDB Path", style=wx.ALIGN_LEFT) 
        m_st_folder_check = wx.StaticText(m_panel, label=u"解析資産フォルダ構成を選択\nPlease select an analysis asset folder structure", style=wx.ALIGN_LEFT) 
        m_st_lib_way = wx.StaticText(m_panel, label=u"ライブラリ名判定方法\nLibrary Name Datermination Method", style=wx.ALIGN_LEFT)
        m_st_lib_id = wx.StaticText(m_panel, label=u"ライブラリID\nLibrary ID", style=wx.ALIGN_LEFT) 
        m_st_have_exname = wx.StaticText(m_panel, label=u"拡張子有無\nWith or Without Extensions", style=wx.ALIGN_LEFT) 
        m_st_have_lib = wx.StaticText(m_panel, label=u"ライブラリ名有無\nWith or Witout Library Name", style=wx.ALIGN_LEFT) 
        m_st_have_member = wx.StaticText(m_panel, label=u"メンバーID有無\nWith or Witout Member ID", style=wx.ALIGN_LEFT) 
        m_st_clean_out_folder = wx.StaticText(m_panel, label=u"資産分類処理出力ファイルクリア\nClear assets classification process output file", style=wx.ALIGN_LEFT) 

        # ! Picker(ファイル選択)
        m_fp_input = wx.DirPickerCtrl(m_panel, message=u"入力フォルダを選択ください/Please select an input folder", style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_fp_input.SetLabel(u"資産入力フォルダ／Asset Input Folder")
        m_fp_output = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder", style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_output.SetLabel(u"結果出力フォルダ／Result Output Folder")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルパス選択/Please select a setup file path", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_fp_setting_file.SetLabel(u"設定ファイルパス/Setup File Path") 
        m_fp_db_file = wx.FilePickerCtrl(m_panel, message=u"言語解析DBを選択ください／Please select a language analysis DB", wildcard=u"*.accdb",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL) 
        m_fp_db_file.SetLabel(u"言語解析DB／Language Analysis DB")

        # ! チェックボックス
        m_cb_is_db_clear = wx.CheckBox(m_panel)
        m_cb_is_db_clear.SetValue(True)
        m_cb_is_folder_clean = wx.CheckBox(m_panel)
        m_cb_is_folder_clean.SetValue(True)

        # ! ComboBox
        # 解析資産フォルダ構成を選択
        list_folder_check = ["個別ライブラリ対応／Individual Library", "複数ライブラリ対応／Multiple Libraries"] 
        combo_box_folder_check = wx.ComboBox(m_panel, -1, value="個別ライブラリ対応／Individual Library", choices=list_folder_check, style=wx.CB_SORT) 
        combo_box_folder_check.Bind(wx.EVT_COMBOBOX, self.check_folder_check)
        # ライブラリ名判定方法
        list_lib_way = ["①直接指定する／Specify Directly", "②サブフォルダ名を使用／Use Subfolder Name", "③ファイル名から取得／Retrieve from File Name"]  
        combo_box_lib_way = wx.ComboBox(m_panel, -1, value="③ファイル名から取得／Retrieve from File Name", choices=list_lib_way, style=wx.CB_SORT) 
        combo_box_lib_way.Bind(wx.EVT_COMBOBOX, self.check_lib_way)
        # 拡張子有無
        list_exname = ["①なし／Without", "②あり（右端)／With (Right End)"] 
        combo_box_exname = wx.ComboBox(m_panel, -1, value="②あり（右端)／With (Right End)", choices=list_exname, style=wx.CB_SORT) 
        # ライブラリ名有無
        list_have_lib = ["①なし／Without", "②あり_正式名／With_Official Name"] 
        combo_box_hava_lib = wx.ComboBox(m_panel, -1, value="②あり_正式名／With_Official Name", choices=list_have_lib, style=wx.CB_SORT) 
        # メンバーID有無
        list_have_member = ["①なし／Without", "②あり_正式名／With_Official Name"] 
        combo_box_hava_member = wx.ComboBox(m_panel, -1, value="②あり_正式名／With_Official Name", choices=list_have_member, style=wx.CB_SORT) 


        # ! 実行ボタン
        m_b_Class = wx.Button(m_panel, label=u"分類実行／Run Classification", size=(200, 30), style=wx.BU_EXACTFIT) 

        # ! TextInput
        text_ctrl_lib_id = wx.TextCtrl(m_panel, -1, style=0)


        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL, border=10)
        m_gb_sizer.Add(m_panel, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL)
        m_gb_sizer.AddGrowableCol(2)

        # 入力フォルダ
        m_panel_gb_sizer.Add(m_st_input, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_input, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_fp_input = m_fp_input
        # 出力フォルダ
        m_panel_gb_sizer.Add(m_st_output, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_output, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_fp_output = m_fp_output
        # 設定ファイルパス
        m_panel_gb_sizer.Add(m_st_setting_file, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_setting_file, pos=(2, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_fp_setting_file = m_fp_setting_file
        # ! DBパス
        m_panel_gb_sizer.Add(m_st_db_path, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_db_file, pos=(3, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_fp_db_file = m_fp_db_file
        # ! 解析資産フォルダ構成を選択
        m_panel_gb_sizer.Add(m_st_folder_check, pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(combo_box_folder_check, pos=(4, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.combo_box_folder_check = combo_box_folder_check
        # ! ライブラリ名判定方法
        m_panel_gb_sizer.Add(m_st_lib_way, pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(combo_box_lib_way, pos=(5, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.combo_box_lib_way = combo_box_lib_way
        # ! ライブラリID
        m_panel_gb_sizer.Add(m_st_lib_id, pos=(6, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(text_ctrl_lib_id, pos=(6, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        text_ctrl_lib_id.SetValue("NA")
        self.text_ctrl_lib_id = text_ctrl_lib_id
        self.m_st_lib_id = m_st_lib_id
        m_st_lib_id.Hide()
        text_ctrl_lib_id.Hide()
        # ! 拡張子有無
        m_panel_gb_sizer.Add(m_st_have_exname, pos=(7, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(combo_box_exname, pos=(7, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.combo_box_exname = combo_box_exname
        # ! ライブラリ名有無
        m_panel_gb_sizer.Add(m_st_have_lib, pos=(8, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(combo_box_hava_lib, pos=(8, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.combo_box_hava_lib = combo_box_hava_lib
        # ! メンバーID有無
        m_panel_gb_sizer.Add(m_st_have_member, pos=(9, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(combo_box_hava_member, pos=(9, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)
        self.combo_box_hava_member = combo_box_hava_member
        # ! RadioButton
        m_panel_gb_sizer.Add(m_st_db_boll, pos=(10, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_cb_is_db_clear, pos=(10, 1), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_cb_is_db_clear = m_cb_is_db_clear
        m_panel_gb_sizer.Add(m_st_clean_out_folder, pos=(11, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_cb_is_folder_clean, pos=(11, 1), flag=wx.EXPAND | wx.ALL, border=10)
        self.m_cb_is_folder_clean = m_cb_is_folder_clean

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_Class, -1, flag=wx.ALIGN_CENTER, border=10)
        m_panel_gb_sizer.Add(vbox, pos=(12, 0), span=(2, 4), flag=wx.EXPAND | wx.ALL)

        m_panel_gb_sizer.AddGrowableCol(3)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        self.SetSizer(m_gb_sizer)
        self.Layout()

        self.Centre(wx.BOTH)




        self.m_cb_is_db_clear = m_cb_is_db_clear

        # Connect Events
        m_b_Class.Bind(wx.EVT_BUTTON, self.on_asset_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def check_lib_way(self, event):
        if self.combo_box_lib_way.GetValue() == "①直接指定する／Specify Directly":
            self.text_ctrl_lib_id.Show()
            self.m_st_lib_id.Show()
        else:
            self.text_ctrl_lib_id.Hide()
            self.m_st_lib_id.Hide()
        self.m_panel.SetSizer(self.m_panel_gb_sizer)
        self.m_gb_sizer.Layout()
        self.m_panel.Layout()

    def check_folder_check(self, event):
        if self.combo_box_folder_check.GetValue() == "複数ライブラリ対応／Multiple Libraries":
            self.combo_box_lib_way.SetValue("②サブフォルダ名を利用／Use Subfolder Name")
            self.combo_box_lib_way.SetBackgroundColour("yellow")
            self.combo_box_hava_lib.SetValue("①なし／Without")
            self.combo_box_hava_lib.SetBackgroundColour("yellow")
        else:
            self.combo_box_lib_way.SetValue("③ファイル名から取得／Retrieve from File Name")
            self.combo_box_lib_way.SetBackgroundColour("white")
            self.combo_box_hava_lib.SetValue("②あり_正式名／With_Official Name")
            self.combo_box_hava_lib.SetBackgroundColour("white")
        self.combo_box_lib_way.Refresh()
        self.combo_box_hava_lib.Refresh()
        self.m_panel.Layout()

    def on_asset_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class ResultFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞顧客データ整理＞解析結果整理／Asset Analysis Support>Organize Client Data>Organize Analysis Results", pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(self, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"入力用ファイル\nFile for Input", style=wx.ALIGN_LEFT)
        m_st_output = wx.StaticText(m_panel, label=u"出力用ファイル\nFile for Output", style=wx.ALIGN_LEFT)
        m_st_setting_file = wx.StaticText(m_panel, label=u"設定ファイルパス\nSetup File Path", style=wx.ALIGN_LEFT)
        m_st_db_bol = wx.StaticText(m_panel, label=u"既存DB削除 \nDelete Existing DB", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_input = wx.FilePickerCtrl(m_panel, message=u"入力用ファイル選択／Please select a file for input", wildcard=u"*.accdb;*.xlsx;*.xlsm",
                                       style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_input.SetLabel(u"出力用ファイル／File for Output")
        m_fp_output = wx.FilePickerCtrl(m_panel, message=u"出力用ファイル選択／Please select a file for output", wildcard=u"*.accdb;*.xlsx;*.xlsm",
                                        style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_output.SetLabel(u"出力用ファイル／File for Output")
        m_fp_setting_file = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file path", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting_file.SetLabel(u"設定ファイルパス／Setup File Path")
        # チェックボックス
        m_cb_is_db_clear = wx.CheckBox(m_panel, label=u"DBの既存データをクリアする場合、チェックを入れる\nCheck the box to clear existing data in the DB")
        m_cb_is_db_clear.SetValue(True)

        # 実行ボタン
        m_b_Result = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL, border=10)
        m_gb_sizer.Add(m_panel, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL)
        m_gb_sizer.AddGrowableCol(2)

        m_panel_gb_sizer.Add(m_st_input, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_input, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_output, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_output, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_db_bol, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_cb_is_db_clear, pos=(2, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_setting_file, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_setting_file, pos=(3, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_Result, 1, flag=wx.ALIGN_CENTER, border=10)
        m_panel_gb_sizer.Add(vbox, pos=(4, 0), span=(2, 4), flag=wx.EXPAND | wx.ALL)

        m_panel_gb_sizer.AddGrowableCol(3)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        self.SetSizer(m_gb_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_input = m_fp_input
        self.m_fp_output = m_fp_output
        self.m_fp_setting_file = m_fp_setting_file
        self.m_cb_is_db_clear = m_cb_is_db_clear

        # Connect Events
        m_b_Result.Bind(wx.EVT_BUTTON, self.on_result_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_result_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class JclResultFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞顧客データ整理＞JCL解析結果／Asset Analysis Support>Organize Client Data>JCL Analysis Results", pos=wx.DefaultPosition,
                          size=wx.Size(800, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(self, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_jcl_db = wx.StaticText(m_panel, label=u"JCL解析済みDB一覧パス\nAnalyzed JCL DB List Path", style=wx.ALIGN_LEFT)
        m_st_output = wx.StaticText(m_panel, label=u"JCL解析結果マージ版出力先フォルダ\nOutput Folder for the Merged Version of JCL Analysis Results", style=wx.ALIGN_LEFT)

        m_dp_jcl_db = wx.DirPickerCtrl(m_panel, message=u"JCL解析済みDB一覧パス選択／Please select an analyzed JCL DB list path", style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_jcl_db.SetLabel(u"JCL解析済みDB一覧パス／Analyzed JCL DB List Path")

        m_fp_output = wx.DirPickerCtrl(m_panel, message=u"JCL解析結果マージ版出力用データ選択／Please select an output folder for the merged version of JCL analysis results",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_output.SetLabel(u"JCL解析結果マージ版出力先フォルダ／Output Folder for the Merged Version of JCL Analysis Results")

        # 実行ボタン
        m_b_Jcl_Result = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL, border=10)
        m_gb_sizer.Add(m_panel, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL)
        m_gb_sizer.AddGrowableCol(2)

        m_panel_gb_sizer.Add(m_st_jcl_db, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_dp_jcl_db, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_output, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_output, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_Jcl_Result, 1, flag=wx.ALIGN_CENTER, border=10)
        m_panel_gb_sizer.Add(vbox, pos=(2, 0), span=(2, 4), flag=wx.EXPAND | wx.ALL)

        m_panel_gb_sizer.AddGrowableCol(3)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        self.SetSizer(m_gb_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_output = m_fp_output
        self.m_dp_jcl_db = m_dp_jcl_db

        # Connect Events
        m_b_Jcl_Result.Bind(wx.EVT_BUTTON, self.on_jcl_result_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_result_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class CobolResultFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞顧客データ整理＞COBOL解析結果／Asset Analysis Support>Organize Client Data>COBOL Analysis Results", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 450), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        # レイアウト定義
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))

        m_panel_gb_sizer = wx.GridBagSizer(10, 0)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(self, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_cobol_db = wx.StaticText(m_panel, label=u"COBOL解析済みDB一覧パス\nAnalyzed COBOL DB List Path", style=wx.ALIGN_LEFT)
        m_st_output = wx.StaticText(m_panel, label=u"COBOL解析結果マージ版出力先フォルダ\nOutput Folder for the Merged Version of COBOL Analysis Results", style=wx.ALIGN_LEFT)
        m_st_call = wx.StaticText(m_panel, label=u"CALL命令限定\nCALL Statement Only", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_dp_cobol_db = wx.DirPickerCtrl(m_panel, message=u"COBOL解析済みDB一覧パス選択／Please select an output destination folder for the merged version of COBOL analysis results",
                                         style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_cobol_db.SetLabel(u"COBOL解析済みDB一覧パス／Analyzed COBOL DB List Path")

        m_fp_output = wx.DirPickerCtrl(m_panel, message=u"COBOL解析結果マージ版出力先フォルダ選択／Please select an output folder for the merged version of COBOL analysis results",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_output.SetLabel(u"COBOL解析結果マージ版出力先フォルダ／Output Folder for the Merged Version of COBOL Analysis Results")

        m_cb_is_call_output = wx.CheckBox(m_panel, label=u"COBOL_CMD情報からCALL命令のみを抽出する場合、チェックを入れる\nCheck the box to extract only CALL statements from COBOL_CMD information")
        m_cb_is_call_output.SetValue(True)

        # 実行ボタン
        m_b_Cobol_Result = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL, border=10)
        m_gb_sizer.Add(m_panel, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL)
        m_gb_sizer.AddGrowableCol(2)

        m_panel_gb_sizer.Add(m_st_cobol_db, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_dp_cobol_db, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_output, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_fp_output, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        m_panel_gb_sizer.Add(m_st_call, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_panel_gb_sizer.Add(m_cb_is_call_output, pos=(2, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_Cobol_Result, 1, flag=wx.ALIGN_CENTER, border=10)
        m_panel_gb_sizer.Add(vbox, pos=(3, 0), span=(2, 4), flag=wx.EXPAND | wx.ALL)

        m_panel_gb_sizer.AddGrowableCol(3)

        m_panel.SetSizer(m_panel_gb_sizer)
        m_panel.Layout()

        self.SetSizer(m_gb_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_output = m_fp_output
        self.m_dp_cobol_db = m_dp_cobol_db
        self.m_cb_is_call_output = m_cb_is_call_output

        # Connect Events
        m_b_Cobol_Result.Bind(wx.EVT_BUTTON, self.on_cobol_result_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_cobol_result_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class DataFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞顧客データ整理／Asset Analysis Support>Organize Client Data", pos=wx.DefaultPosition,
                          size=wx.Size(600, 460), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_Result = wx.Button(m_panel, label=u"解析結果整理\nOrganize Analysis Results", style=wx.BU_EXACTFIT)
        m_b_Jcl_Result = wx.Button(m_panel, label=u"JCL解析結果マージ\nMerging JCL Analysis Results", style=wx.BU_EXACTFIT)
        m_b_Cobol_Result = wx.Button(m_panel, label=u"COBOL解析結果マージ\nMerging COBOL Analysis Results", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_Result, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_Jcl_Result, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_Cobol_Result, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_Result.Bind(wx.EVT_BUTTON, self.on_result_click)
        m_b_Jcl_Result.Bind(wx.EVT_BUTTON, self.on_jcl_result_click)
        m_b_Cobol_Result.Bind(wx.EVT_BUTTON, self.on_cobol_result_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def on_result_click(self, event):
        event.Skip()

    def on_jcl_result_click(self, event):
        event.Skip()

    def on_cobol_result_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MachineDbFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞顧客用DBデータ準備／Asset Analysis Support>Processing of Asset Analysis Results>Prepare Data for ClientDB", pos=wx.DefaultPosition,
                          size=wx.Size(900, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_db_out = wx.StaticText(m_panel, label=u"資産解析済みDB格納フォルダ\nAnalyzed Asset DB Storage Folder", style=wx.ALIGN_LEFT)
        m_st_bol = wx.StaticText(m_panel, label=u"DB初期化\nDB Initialization", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_db_out = wx.DirPickerCtrl(m_panel, message=u"資産解析済みDB格納フォルダを選択ください／Please select an analyzed asset DB storage folder",
                                       style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_db_out.SetLabel(u"資産解析済みDB格納フォルダ／Analyzed Asset DB Storage Folder")

        m_cb_bol = wx.CheckBox(m_panel, label=u"顧客別DBを初期化してからデータを追加する場合、チェックを入れる\nCheck the box to initialize the ClientDB before adding data")
        m_cb_bol.SetValue(True)

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_db_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_db_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_bol, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_cb_bol, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_db_out = m_dp_db_out
        self.m_cb_bol = m_cb_bol

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class PedDamFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞PED-DAM解析／Asset Analysis Support>Processing of Asset Analysis Results>PED-DAM Analysis", pos=wx.DefaultPosition,
                          size=wx.Size(800, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)

        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"事前解析結果出力先フォルダ\nOutput Folder for Pre-Analysis Results", style=wx.ALIGN_LEFT)
        m_st_ped = wx.StaticText(m_panel, label=u"PED格納パス\nPED Storage Path", style=wx.ALIGN_LEFT)
        m_st_definition = wx.StaticText(m_panel, label=u"定義体格納パス\nDefined Entities Storage Path", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"事前解析結果出力先フォルダを選択ください／Please select an output folder for pre-analysis results",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"事前解析結果出力先フォルダ／Output Folder for Pre-Analysis Results")
        m_dp_ped = wx.DirPickerCtrl(m_panel, message=u"PED格納パスを選択ください／Please select a PED storage path",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_ped.SetLabel(u"PED格納パス／PED Storage Path")
        m_dp_definition = wx.DirPickerCtrl(m_panel, message=u"定義体格納パスを選択ください／Please select a defined entities storage path",
                                           style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_definition.SetLabel(u"定義体格納パス／Defined Entities Storage Path")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_ped, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_ped, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_definition, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_definition, pos=(4, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(5, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out
        self.m_dp_ped = m_dp_ped
        self.m_dp_definition = m_dp_definition

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MachineBeforeFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞資産解析結果加工事前解析／Asset Analysis Support>Processing of Asset Analysis Results>Pre-Processing of Asset Analysis Results", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"事前解析結果出力先フォルダ\nOutput Folder for Pre-Analysis Results", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"事前解析結果出力先フォルダを選択ください／Please select an output folder for pre-analysis results",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"事前解析結果出力先フォルダ／Output Folder for Pre-Analysis Results")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineReceiptFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞受領資産一覧登録／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Received Assets List Registration",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1200, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"受領資産一覧\nReceived Assets List", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.FilePickerCtrl(m_panel, message=u"受領資産一覧を選択ください／Please select a received assets list", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"受領資産一覧／Received Assets List")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineCustomerFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞顧客別資産関連性登録／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Asset Relationship Registration by Client",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_maji = wx.StaticText(m_panel, label=u"関連性マージ版\nRelationship Merged Document", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB\／ClientDB")
        m_dp_out = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"設定ファイル／Setup File")
        m_dp_maji = wx.FilePickerCtrl(m_panel, message=u"関連性マージ版を選択ください／Please select a relationship merged document", wildcard=u"*.xlsx;*.xlsm",
                                      style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_maji.SetLabel(u"関連性マージ版／Relationship Merged Document")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_maji, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_maji, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out
        self.m_dp_maji = m_dp_maji

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineStartFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞起点資産分割／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Starting Point Asset Split",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_setting = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"起点資産分割後出力先フォルダ\nOutput Folder after Spliting the Starting Point Asset", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_dp_setting = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                         style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_setting.SetLabel(u"設定ファイル／Setup File")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"起点資産分割後出力先フォルダを選択ください／Please select an output folder after splitting the starting point asset",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"起点資産分割後出力先フォルダ／Output Folder after Spliting the Starting Point Asset")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_setting, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_setting, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_dp_setting = m_dp_setting
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineTestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞テスト実施単位登録／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Test Execution Unit Registration",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"テスト実施単位ファイル\nTest Execution Unit File", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.FilePickerCtrl(m_panel, message=u"テスト実施単位ファイルを選択ください／Please select a test execution unit file", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"テスト実施単位ファイル／Test Execution Unit File")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineAssetsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞資産階層図出力／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Asset Hierarchy Diagram Output",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"階層図出力先フォルダ\nOutput Folder for Hierarchy Diagram", style=wx.ALIGN_LEFT)
        m_st_bol = wx.StaticText(m_panel, label=u"作成ファイル分割\nCreate File Split", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"階層図出力先フォルダを選択ください／Please select an output folder for hierarchy diagram",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"階層図出力先フォルダ／Output Folder for Hierarchy Diagram")

        m_cb_bol = wx.CheckBox(m_panel, label=u"起点資産ごとに出力ファイルを分割する場合、チェックを入れる\nCheck the box to split Asset file by starting point output")
        m_cb_bol.SetValue(True)

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_bol, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_cb_bol, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out
        self.m_cb_bol = m_cb_bol

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class OnlineRelatedFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞関連資産出力／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Related Asset Output",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"関連資産出力先フォルダ\nOutput Folder for Related Assets", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"関連資産出力先フォルダを選択ください／Please select an output folder for related assets",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"関連資産出力先フォルダ／Output Folder for Related Assets")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class StarumFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成＞逆階層図出力／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation>Reverse Hierarchy Diagram Output", pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        self.GetMenuBar()
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_input = wx.StaticText(m_panel, label=u"資産関連性調査結果\nAsset Relationship Research Results", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"出力フォルダ\nOutput Folder", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_input = wx.FilePickerCtrl(m_panel, message=u"資産関連性調査結果を選択ください／Please select an asset relationship research results", wildcard=u"*.xlsx;*.xlsm",
                                              style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_input.SetLabel(u"資産関連性調査結果／Asset Relationship Research Results")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"出力フォルダを選択ください／Please select an output folder",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"出力フォルダ／Output Folder")

        # 実行ボタン
        m_b_jcl_out = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_input, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_input, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_jcl_out, 1, flag=wx.ALIGN_CENTER, border=10)

        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_input = m_fp_input
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_jcl_out.Bind(wx.EVT_BUTTON, self.on_jcl_out_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_jcl_out_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MachineOnlineFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞オンライン解析結果作成／Asset Analysis Support>Processing of Asset Analysis Results>Online Analysis Result Generation", pos=wx.DefaultPosition,
                          size=wx.Size(950, 650), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_receipt = wx.Button(m_panel, label=u"受領資産一覧登録\nReceived Assets List Registration", style=wx.BU_EXACTFIT)
        m_b_customer = wx.Button(m_panel, label=u"顧客別資産関連性登録\nAsset Relationship Registration by Client", style=wx.BU_EXACTFIT)
        m_b_start = wx.Button(m_panel, label=u"起点資産分割\nStarting Point Asset Split", style=wx.BU_EXACTFIT)
        m_b_test = wx.Button(m_panel, label=u"テスト実施単位登録\nTest Execution Unit Registration", style=wx.BU_EXACTFIT)
        m_b_assets = wx.Button(m_panel, label=u"資産階層図出力\nAsset Hierarchy Diagram Output", style=wx.BU_EXACTFIT)
        m_b_stratum = wx.Button(m_panel, label=u"逆階層図出力\nReverse Hierarchy Diagram Output", style=wx.BU_EXACTFIT)
        m_b_related = wx.Button(m_panel, label=u"関連資産出力\nRelated Asset Output", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_receipt, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_customer, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_start, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_test, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_assets, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_stratum, pos=(6, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_related, pos=(7, 0), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_receipt.Bind(wx.EVT_BUTTON, self.on_receipt_click)
        m_b_customer.Bind(wx.EVT_BUTTON, self.on_customer_click)
        m_b_start.Bind(wx.EVT_BUTTON, self.on_start_click)
        m_b_test.Bind(wx.EVT_BUTTON, self.on_test_click)
        m_b_assets.Bind(wx.EVT_BUTTON, self.on_assets_click)
        m_b_stratum.Bind(wx.EVT_BUTTON, self.on_stratum_click)
        m_b_related.Bind(wx.EVT_BUTTON, self.on_related_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_receipt_click(self, event):
        event.Skip()

    def on_customer_click(self, event):
        event.Skip()

    def on_start_click(self, event):
        event.Skip()

    def on_test_click(self, event):
        event.Skip()

    def on_assets_click(self, event):
        event.Skip()

    def on_stratum_click(self, event):
        event.Skip()

    def on_related_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class BatchDataFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞バッチ解析結果作成＞DATA_DSN情報登録／Asset Analysis Support>Processing of Asset Analysis Results>Batch Analysis Result Generation>DATA_DSN Information Registration",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"DATA_DSN情報一覧\nDATA_DSN Information List", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.FilePickerCtrl(m_panel, message=u"DATA_DNS情報一覧を選択ください／Please select a DATA_DNS information list", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"DATA_DSN情報一覧／DATA_DSN Information List")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class BatchStartFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞バッチ解析結果作成＞起点資産分割／Asset Analysis Support>Processing of Asset Analysis Results>Batch Analysis Result Generation>Starting Point Asset Split",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_setting = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"起点資産分割後出力先フォルダ\nOutput Folder after Spliting The Starting Point Asset", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_setting = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                         style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting.SetLabel(u"設定ファイル／Setup File")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"起点資産分割後出力先フォルダを選択ください／Please select an output folder after splitting the starting point asset",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"起点資産分割後出力先フォルダ／Output Folder after Spliting The Starting Point Asset")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_setting, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_setting = m_fp_setting
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class BatchTestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞バッチ解析結果作成＞テスト実施単位登録／Asset Analysis Support>Processing of Asset Analysis Results>Batch Analysis Result Generation>Test Execution Unit Registration",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"テスト実施単位ファイル\nTest Execution Unit File", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_dp_out = wx.FilePickerCtrl(m_panel, message=u"テスト実施単位ファイル／Test execution unit file", wildcard=u"*.xlsx;*.xlsm",
                                     style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"テスト実施単位ファイル／Test Execution Unit File")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(3, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class BatchOutFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞バッチ解析結果作成＞バッチ入出力情報出力／Asset Analysis Support>Processing of Asset Analysis Results>Batch Analysis Result Generation>Batch I/O Information Output",
                          pos=wx.DefaultPosition,
                          size=wx.Size(1250, 350), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(9, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 文言
        m_st_customer_db = wx.StaticText(m_panel, label=u"顧客別DB\nClientDB", style=wx.ALIGN_LEFT)
        m_st_setting = wx.StaticText(m_panel, label=u"設定ファイル\nSetup File", style=wx.ALIGN_LEFT)
        m_st_out = wx.StaticText(m_panel, label=u"バッチ入出力情報出力先フォルダ\nOutput Folder for Batch I/O Information", style=wx.ALIGN_LEFT)

        # Picker(ファイル選択)
        m_fp_customer_db = wx.FilePickerCtrl(m_panel, message=u"顧客別DBを選択ください／Please select a ClientDB", wildcard=u"*.accdb",
                                             style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_customer_db.SetLabel(u"顧客別DB／ClientDB")
        m_fp_setting = wx.FilePickerCtrl(m_panel, message=u"設定ファイルを選択ください／Please select a setup file", wildcard=u"*.xlsx;*.xlsm",
                                         style=wx.FLP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_fp_setting.SetLabel(u"設定ファイル／Setup File")
        m_dp_out = wx.DirPickerCtrl(m_panel, message=u"バッチ入出力情報出力先フォルダを選択ください／Please select an output destination folder for batch I/O information",
                                    style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        m_dp_out.SetLabel(u"バッチ入出力情報出力先フォルダ／Output Folder for Batch I/O Information")

        m_b_analysis = wx.Button(m_panel, label=u"解析実行／Run Analysis", size=(200, 30), style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_st_customer_db, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_customer_db, pos=(1, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_setting, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_fp_setting, pos=(2, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_st_out, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
        m_gb_sizer.Add(m_dp_out, pos=(3, 2), span=(1, 5), flag=wx.EXPAND | wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(m_b_analysis, 1, flag=wx.ALIGN_CENTER, border=10)
        m_gb_sizer.Add(vbox, pos=(4, 1), span=(2, 6), flag=wx.EXPAND | wx.ALL)

        m_gb_sizer.AddGrowableCol(6)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_fp_customer_db = m_fp_customer_db
        self.m_fp_setting = m_fp_setting
        self.m_dp_out = m_dp_out

        # Connect Events
        m_b_analysis.Bind(wx.EVT_BUTTON, self.on_analysis_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_analysis_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MachineBatchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工＞バッチ解析結果作成／Asset Analysis Support>Processing of Asset Analysis Results>Batch Analysis Result Generation", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 460), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_data = wx.Button(m_panel, label=u"DATA_DSN情報登録\nDATA_DSN Information Registration", style=wx.BU_EXACTFIT)
        m_b_start = wx.Button(m_panel, label=u"起点資産分割\nStarting Point Asset Split", style=wx.BU_EXACTFIT)
        m_b_test = wx.Button(m_panel, label=u"テスト実施単位登録\nTest Execution Unit Registration", style=wx.BU_EXACTFIT)
        m_b_out = wx.Button(m_panel, label=u"バッチ入出力情報出力\nBatch I/O Information Output", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_data, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_start, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_test, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=15)
        m_gb_sizer.Add(m_b_out, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=15)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_data.Bind(wx.EVT_BUTTON, self.on_data_click)
        m_b_start.Bind(wx.EVT_BUTTON, self.on_start_click)
        m_b_test.Bind(wx.EVT_BUTTON, self.on_test_click)
        m_b_out.Bind(wx.EVT_BUTTON, self.on_batch_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_data_click(self, event):
        event.Skip()

    def on_start_click(self, event):
        event.Skip()

    def on_test_click(self, event):
        event.Skip()

    def on_batch_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()


class MachineFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"棚卸サポート＞資産解析結果加工／Asset Analysis Support>Processing of Asset Analysis Results", pos=wx.DefaultPosition,
                          size=wx.Size(600, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL)
        # logo設定
        self.SetIcon(_get_logo())

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour('TURQUOISE')

        m_bx_sizer = wx.BoxSizer(wx.VERTICAL)
        m_gb_sizer = wx.GridBagSizer(10, 0)

        m_panel = wx.Panel(self)
        m_panel.SetFont(wx.Font(12, 70, 90, 90, False, "Meiryo"))
        m_bx_sizer.Add(m_panel, 1, wx.EXPAND | wx.ALL, 10)

        # 戻るボタン
        m_bb_back = wx.BitmapButton(m_panel, bitmap=getattr(images, "back").GetBitmap())

        # 実行ボタン
        m_b_db = wx.Button(m_panel, label=u"顧客用DBデータ準備\nPrepare Data for ClientDB", style=wx.BU_EXACTFIT)
        m_b_ped_dam = wx.Button(m_panel, label=u"PED-DAM解析\nPED-DAM Analysis", style=wx.BU_EXACTFIT)
        # m_b_psb = wx.Button(m_panel, label=u"PSB解析\nPSB Analysis", style=wx.BU_EXACTFIT) # PSBボタンを非表示にする
        m_b_before = wx.Button(m_panel, label=u"資産解析結果加工事前解析\nPre-Processing of Asset Analysis Results", style=wx.BU_EXACTFIT)
        m_b_online = wx.Button(m_panel, label=u"オンライン解析結果作成\nOnline Analysis Result Generation", style=wx.BU_EXACTFIT)
        m_b_batch = wx.Button(m_panel, label=u"バッチ解析結果作成\nBatch Analysis Result Generation", style=wx.BU_EXACTFIT)

        m_gb_sizer.Add(m_bb_back, pos=(0, 0), flag=wx.ALL)

        m_gb_sizer.Add(m_b_db, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_ped_dam, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=10)
        # m_gb_sizer.Add(m_b_psb, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=10) # PSBボタンを非表示にする
        m_gb_sizer.Add(m_b_before, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_online, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=10)
        m_gb_sizer.Add(m_b_batch, pos=(5, 0), flag=wx.EXPAND | wx.ALL, border=10)

        m_gb_sizer.AddGrowableCol(0)
        m_panel.SetSizerAndFit(m_gb_sizer)

        self.SetSizer(m_bx_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        m_b_db.Bind(wx.EVT_BUTTON, self.on_db_click)
        m_b_ped_dam.Bind(wx.EVT_BUTTON, self.on_ped_dam_click)
        # m_b_psb.Bind(wx.EVT_BUTTON, self.on_psb_click) # PSBボタンを非表示にする
        m_b_before.Bind(wx.EVT_BUTTON, self.on_before_click)
        m_b_online.Bind(wx.EVT_BUTTON, self.on_online_click)
        m_b_batch.Bind(wx.EVT_BUTTON, self.on_batch_click)
        m_bb_back.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, _exit_sys)

    def __del__(self):
        pass

    def on_db_click(self, event):
        event.Skip()

    def on_ped_dam_click(self, event):
        event.Skip()

    def on_psb_click(self, event):
        event.Skip()

    def on_before_click(self, event):
        event.Skip()

    def on_online_click(self, event):
        event.Skip()

    def on_batch_click(self, event):
        event.Skip()

    def on_close(self, event):
        event.Skip()
