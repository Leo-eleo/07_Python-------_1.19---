# -*- coding: utf-8 -*-
import os
import wx

from common import executeCmdStr, checkSub, executeJavaCmdStr
from ui import ClassAssetFrame, AnalysisFrame, MainFrame, DataFrame, MachineFrame, JclFrame, ProcFrame, SysinFrame, \
    CobolFrame, JclOutFrame, ResultFrame, JclResultFrame, CobolResultFrame, RelevanceFrame, RelevanceAnalysisFrame, \
    RelevanceMajiFrame, RelevanceCompareFrame, MachineDbFrame, MachineBeforeFrame, MachineOnlineFrame, \
    MachineBatchFrame, OnlineReceiptFrame, OnlineCustomerFrame, OnlineStartFrame, OnlineTestFrame, OnlineAssetsFrame, \
    OnlineRelatedFrame, BatchDataFrame, BatchStartFrame, BatchTestFrame, BatchOutFrame, MemberSplitFrame, PgmFrame, \
    PliFrame, NaturalFrame, GrepFrame, NativePliFrame, PliCmdFrame, PedDamFrame, RationalizationFrame, StarumFrame, \
    ClistFrame, CParseFrame


class MainService(MainFrame):
    s_class_asset = None
    s_analysis = None
    s_jcl = None
    s_proc = None
    s_sysin = None
    s_pli = None
    s_native_pli = None
    s_pli_cmd = None
    s_cobol = None
    s_natrual = None
    s_clist = None
    s_c_parse = None
    s_rationalization = None
    s_pgm = None
    s_jclout = None
    s_grep = None
    s_memberSplit = None
    s_result = None
    s_data = None
    s_jcl_result = None
    s_cobol_result = None
    s_relevance = None
    s_relevance_analysis = None
    s_relevance_maji = None
    s_relevance_compare = None
    s_machine = None
    s_machine_db = None
    s_machine_before = None
    s_machine_online = None
    s_starum = None
    s_online_receipt = None
    s_online_customer = None
    s_online_start = None
    s_online_test = None
    s_online_assets = None
    s_online_related = None
    s_machine_batch = None
    s_batch_data = None
    s_batch_start = None
    s_batch_test = None
    s_batch_out = None
    s_ped_dam = None

    def on_class_asset_click(self, event):
        if self.s_class_asset is None:
            self.s_class_asset = ClassAssetService(self)
        self.s_class_asset.Show()
        self.Hide()

    def on_class_asset_close(self):
        self.s_class_asset.Hide()
        self.Show()

    def on_class_asset_process(self):
        pass

    def on_analysis_click(self, event):
        if self.s_analysis is None:
            self.s_analysis = AnalysisService(self)
        self.s_analysis.Show()
        self.Hide()

    def on_relevance_click(self, event):
        if self.s_relevance is None:
            self.s_relevance = RelevanceService(self)
        self.s_relevance.Show()
        self.Hide()

    def on_arrange_data_click(self, event):
        if self.s_data is None:
            self.s_data = DataService(self)
        self.s_data.Show()
        self.Hide()

    def on_machine_result_click(self, event):
        if self.s_machine is None:
            self.s_machine = MachineService(self)
        self.s_machine.Show()
        self.Hide()

    def on_jcl_click(self):
        if self.s_jcl is None:
            self.s_jcl = JclService(self)
        self.s_jcl.Show()
        self.s_analysis.Hide()

    def on_proc_click(self):
        if self.s_proc is None:
            self.s_proc = ProcService(self)
        self.s_proc.Show()
        self.s_analysis.Hide()

    def on_sysin_click(self):
        if self.s_sysin is None:
            self.s_sysin = SysinService(self)
        self.s_sysin.Show()
        self.s_analysis.Hide()

    def on_natvie_pli_click(self):
        if self.s_native_pli is None:
            self.s_native_pli = NativePliService(self)
        self.s_native_pli.Show()
        self.s_pli.Hide()

    def on_rationalization_click(self):
        if self.s_rationalization is None:
            self.s_rationalization = RationalizationService(self)
        self.s_rationalization.Show()
        self.s_pli.Hide()

    def on_pli_cmd_click(self):
        if self.s_pli_cmd is None:
            self.s_pli_cmd = PliCmdService(self)
        self.s_pli_cmd.Show()
        self.s_pli.Hide()

    def on_pli_click(self):
        if self.s_pli is None:
            self.s_pli = PliService(self)
        self.s_pli.Show()
        self.s_pgm.Hide()

    def on_natrual_click(self):
        if self.s_natrual is None:
            self.s_natrual = NaturalService(self)
        self.s_natrual.Show()
        self.s_pgm.Hide()

    def on_clist_click(self):
        if self.s_clist is None:
            self.s_clist = ClistService(self)
        self.s_clist.Show()
        self.s_pgm.Hide()

    def on_c_parse_click(self):
        if self.s_c_parse is None:
            self.s_c_parse = CParseService(self)
        self.s_c_parse.Show()
        self.s_pgm.Hide()

    def on_cobol_click(self):
        if self.s_cobol is None:
            self.s_cobol = CobolService(self)
        self.s_cobol.Show()
        self.s_pgm.Hide()

    def on_pgm_click(self):
        if self.s_pgm is None:
            self.s_pgm = PgmService(self)
        self.s_pgm.Show()
        self.s_analysis.Hide()

    def on_jclout_click(self):
        if self.s_jclout is None:
            self.s_jclout = JclOutService(self)
        self.s_jclout.Show()
        self.s_analysis.Hide()

    def on_memberSplit_click(self):
        if self.s_memberSplit is None:
            self.s_memberSplit = MemberSplitService(self)
        self.s_memberSplit.Show()
        self.s_analysis.Hide()

    def on_grep_click(self):
        if self.s_grep is None:
            self.s_grep = GrepService(self)
        self.s_grep.Show()
        self.s_analysis.Hide()

    def on_result_click(self):
        if self.s_result is None:
            self.s_result = ResultService(self)
        self.s_result.Show()
        self.s_data.Hide()

    def on_jcl_result_click(self):
        if self.s_jcl_result is None:
            self.s_jcl_result = JclResultService(self)
        self.s_jcl_result.Show()
        self.s_data.Hide()

    def on_cobol_result_click(self):
        if self.s_cobol_result is None:
            self.s_cobol_result = CobolResultService(self)
        self.s_cobol_result.Show()
        self.s_data.Hide()

    def on_relevance_analysis_click(self):
        if self.s_relevance_analysis is None:
            self.s_relevance_analysis = RelevanceAnalysisService(self)
        self.s_relevance_analysis.Show()
        self.s_relevance.Hide()

    def on_relevance_maji_click(self):
        if self.s_relevance_maji is None:
            self.s_relevance_maji = RelevanceMajiService(self)
        self.s_relevance_maji.Show()
        self.s_relevance.Hide()

    def on_relevance_compare_click(self):
        if self.s_relevance_compare is None:
            self.s_relevance_compare = RelevanceCompareService(self)
        self.s_relevance_compare.Show()
        self.s_relevance.Hide()

    def on_machine_db_click(self):
        if self.s_machine_db is None:
            self.s_machine_db = MachineDbService(self)
        self.s_machine_db.Show()
        self.s_machine.Hide()

    def on_machine_before_click(self):
        if self.s_machine_before is None:
            self.s_machine_before = MachineBeforeService(self)
        self.s_machine_before.Show()
        self.s_machine.Hide()

    def on_machine_online_click(self):
        if self.s_machine_online is None:
            self.s_machine_online = MachineOnlineService(self)
        self.s_machine_online.Show()
        self.s_machine.Hide()

    def on_starum_click(self):
        if self.s_starum is None:
            self.s_starum = StarumService(self)
        self.s_starum.Show()
        self.s_machine_online.Hide()

    def on_online_receipt_click(self):
        if self.s_online_receipt is None:
            self.s_online_receipt = OnlineReceiptService(self)
        self.s_online_receipt.Show()
        self.s_machine_online.Hide()

    def on_online_customer_click(self):
        if self.s_online_customer is None:
            self.s_online_customer = OnlineCustomerService(self)
        self.s_online_customer.Show()
        self.s_machine_online.Hide()

    def on_online_start_click(self):
        if self.s_online_start is None:
            self.s_online_start = OnlineStartService(self)
        self.s_online_start.Show()
        self.s_machine_online.Hide()

    def on_online_test_click(self):
        if self.s_online_test is None:
            self.s_online_test = OnlineTestService(self)
        self.s_online_test.Show()
        self.s_machine_online.Hide()

    def on_online_assets_click(self):
        if self.s_online_assets is None:
            self.s_online_assets = OnlineAssetsService(self)
        self.s_online_assets.Show()
        self.s_machine_online.Hide()

    def on_online_related_click(self):
        if self.s_online_related is None:
            self.s_online_related = OnlineRelatedService(self)
        self.s_online_related.Show()
        self.s_machine_online.Hide()

    def on_machine_batch_click(self):
        if self.s_machine_batch is None:
            self.s_machine_batch = MachineBatchService(self)
        self.s_machine_batch.Show()
        self.s_machine.Hide()

    def on_batch_data_click(self):
        if self.s_batch_data is None:
            self.s_batch_data = BatchDataService(self)
        self.s_batch_data.Show()
        self.s_machine_batch.Hide()

    def on_batch_start_click(self):
        if self.s_batch_start is None:
            self.s_batch_start = BatchStartService(self)
        self.s_batch_start.Show()
        self.s_machine_batch.Hide()

    def on_batch_test_click(self):
        if self.s_batch_test is None:
            self.s_batch_test = BatchTestService(self)
        self.s_batch_test.Show()
        self.s_machine_batch.Hide()

    def on_ped_dam_click(self):
        if self.s_ped_dam is None:
            self.s_ped_dam = PedDamService(self)
        self.s_ped_dam.Show()
        self.s_machine.Hide()

    def on_batch_out_click(self):
        if self.s_batch_out is None:
            self.s_batch_out = BatchOutService(self)
        self.s_batch_out.Show()
        self.s_machine_batch.Hide()

    def on_relevance_close(self):
        self.s_relevance.Hide()
        self.Show()

    def on_analysis_close(self):
        self.s_analysis.Hide()
        self.Show()

    def on_data_close(self):
        self.s_data.Hide()
        self.Show()

    def on_machine_close(self):
        self.s_machine.Hide()
        self.Show()

    def on_jcl_close(self):
        self.s_jcl.Hide()
        self.s_analysis.Show()

    def on_proc_close(self):
        self.s_proc.Hide()
        self.s_analysis.Show()

    def on_sysin_close(self):
        self.s_sysin.Hide()
        self.s_analysis.Show()

    def on_pli_cmd_close(self):
        self.s_pli_cmd.Hide()
        self.s_pli.Show()

    def on_native_pli_close(self):
        self.s_native_pli.Hide()
        self.s_pli.Show()

    def on_rationalization_close(self):
        self.s_rationalization.Hide()
        self.s_pli.Show()

    def on_pli_close(self):
        self.s_pli.Hide()
        self.s_pgm.Show()

    def on_natrual_close(self):
        self.s_natrual.Hide()
        self.s_pgm.Show()

    def on_clist_close(self):
        self.s_clist.Hide()
        self.s_pgm.Show()

    def on_c_parse_close(self):
        self.s_c_parse.Hide()
        self.s_pgm.Show()

    def on_cobol_close(self):
        self.s_cobol.Hide()
        self.s_pgm.Show()

    def on_pgm_close(self):
        self.s_pgm.Hide()
        self.s_analysis.Show()

    def on_jclout_close(self):
        self.s_jclout.Hide()
        self.s_analysis.Show()

    def on_memberSplit_close(self):
        self.s_memberSplit.Hide()
        self.s_analysis.Show()

    def on_grep_close(self):
        self.s_grep.Hide()
        self.s_analysis.Show()

    def on_result_close(self):
        self.s_result.Hide()
        self.s_data.Show()

    def on_jcl_result_close(self):
        self.s_jcl_result.Hide()
        self.s_data.Show()

    def on_cobol_result_close(self):
        self.s_cobol_result.Hide()
        self.s_data.Show()

    def on_relevance_analysis_close(self):
        self.s_relevance_analysis.Hide()
        self.s_relevance.Show()

    def on_relevance_maji_close(self):
        self.s_relevance_maji.Hide()
        self.s_relevance.Show()

    def on_relevance_compare_close(self):
        self.s_relevance_compare.Hide()
        self.s_relevance.Show()

    def on_machine_db_close(self):
        self.s_machine_db.Hide()
        self.s_machine.Show()

    def on_machine_before_close(self):
        self.s_machine_before.Hide()
        self.s_machine.Show()

    def on_machine_online_close(self):
        self.s_machine_online.Hide()
        self.s_machine.Show()

    def on_starum_close(self):
        self.s_starum.Hide()
        self.s_machine_online.Show()

    def on_online_receipt_close(self):
        self.s_online_receipt.Hide()
        self.s_machine_online.Show()

    def on_online_customer_close(self):
        self.s_online_customer.Hide()
        self.s_machine_online.Show()

    def on_online_start_close(self):
        self.s_online_start.Hide()
        self.s_machine_online.Show()

    def on_online_test_close(self):
        self.s_online_test.Hide()
        self.s_machine_online.Show()

    def on_online_assets_close(self):
        self.s_online_assets.Hide()
        self.s_machine_online.Show()

    def on_online_related_close(self):
        self.s_online_related.Hide()
        self.s_machine_online.Show()

    def on_machine_batch_close(self):
        self.s_machine_batch.Hide()
        self.s_machine.Show()

    def on_batch_data_close(self):
        self.s_batch_data.Hide()
        self.s_machine_batch.Show()

    def on_batch_start_close(self):
        self.s_batch_start.Hide()
        self.s_machine_batch.Show()

    def on_batch_test_close(self):
        self.s_batch_test.Hide()
        self.s_machine_batch.Show()

    def on_ped_dam_close(self):
        self.s_ped_dam.Hide()
        self.s_machine.Show()

    def on_batch_out_close(self):
        self.s_batch_out.Hide()
        self.s_machine_batch.Show()


class ClassAssetService(ClassAssetFrame):
    def on_close(self, event):
        main.on_class_asset_close()

    def on_asset_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Asset_Class",
                               "asset_class.py")
        checkSub(["cmd", "dir", "dir", "excel", "db", "text", "text", "text", "text", "text", "text", "bool", "bool"],
                executeCmdStr,
                cmdPath, self.m_fp_input, self.m_fp_output, self.m_fp_setting_file, self.m_fp_db_file,
                self.combo_box_folder_check, self.combo_box_lib_way, self.text_ctrl_lib_id,
                self.combo_box_exname, self.combo_box_hava_lib, self.combo_box_hava_member,
                self.m_cb_is_db_clear.IsChecked(), self.m_cb_is_folder_clean.IsChecked()
                )

class RelevanceService(RelevanceFrame):
    def on_analysis_click(self, event):
        main.on_relevance_analysis_click()

    def on_maji_click(self, event):
        main.on_relevance_maji_click()

    def on_compare_click(self, event):
        main.on_relevance_compare_click()

    def on_close(self, event):
        main.on_relevance_close()


class RelevanceAnalysisService(RelevanceAnalysisFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Relation_Analysis",
                               "relation_analysis_main.py")
        checkSub(["cmd", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_setting_file, self.m_dp_jcl)

    def on_close(self, event):
        main.on_relevance_analysis_close()


class RelevanceMajiService(RelevanceMajiFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Relation_Analysis",
                               "relation_merge.py")
        checkSub(["cmd", "dir", "dir"], executeCmdStr, cmdPath, self.m_fp_out, self.m_dp_jcl)

    def on_close(self, event):
        main.on_relevance_maji_close()


class RelevanceCompareService(RelevanceCompareFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Relation_Analysis",
                               "merge_get_difference.py")
        checkSub(["cmd", "excel", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_new,
                 self.m_fp_old, self.m_dp_jcl)

    def on_close(self, event):
        main.on_relevance_compare_close()


class GrepService(GrepFrame):
    def on_result_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "GREP_TOOL",
                               "inside-0.0.1-SNAPSHOT.jar")
        checkSub(["cmd", "excel", "dir"], executeJavaCmdStr, cmdPath, self.m_fp_setting_file, self.m_dp_out)

    def on_close(self, event):
        main.on_grep_close()


class AnalysisService(AnalysisFrame):
    def on_jcl_analysis_click(self, e):
        main.on_jcl_click()

    def on_proc_analysis_click(self, e):
        main.on_proc_click()

    def on_sysin_analysis_click(self, e):
        main.on_sysin_click()

    def on_pgm_analysis_click(self, e):
        main.on_pgm_click()

    def on_jcl_out_click(self, event):
        main.on_jclout_click()

    def on_member_spilt_click(self, event):
        main.on_memberSplit_click()

    def on_grep_click(self, event):
        main.on_grep_click()

    def on_close(self, event):
        main.on_analysis_close()


class JclService(JclFrame):
    def on_jcl_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "JCL解析",
                               "JCL_analysis_main.py")
        checkSub(["cmd", "db", "dir", "excel"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_jcl, self.m_fp_setting_file)

    def on_close(self, event):
        main.on_jcl_close()


class ProcService(ProcFrame):
    def on_proc_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "JCL解析",
                               "JCL_analysis_main.py")
        checkSub(["cmd", "db", "dir", "excel"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_proc, self.m_fp_setting_file)

    def on_close(self, event):
        main.on_proc_close()


class SysinService(SysinFrame):
    def on_sysin_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "JCL解析",
                               "External_SYSIN_main.py")
        checkSub(["cmd", "db", "dir", "excel"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_sysin, self.m_fp_setting_file)

    def on_close(self, event):
        main.on_sysin_close()


class NaturalService(NaturalFrame):
    def on_natrual_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Natural解析",
                               "COBOL_analysis_main_all_folder.py")
        checkSub(["cmd", "db", "dir", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_natrual, self.m_fp_setting_file, self.m_dp_db_out)

    def on_close(self, event):
        main.on_natrual_close()


class ClistService(ClistFrame):
    def on_clist_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Clist解析",
                               "Clist_Analysis_main.py")
        checkSub(["cmd", "db", "dir", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_clist, self.m_fp_setting_file, self.m_dp_db_out)

    def on_close(self, event):
        main.on_clist_close()


class CParseService(CParseFrame):
    def on_c_parse_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "C言語解析", "src",
                               "c_parse_main.py")
        # Check is rm 72-80
        is_rm = ""
        if self.m_cb_is_rm_72_80.IsChecked():
            is_rm = "-R"
        checkSub(["cmd", "dir", "db", "excel", "dir", "option"], executeCmdStr, cmdPath, self.m_dp_c_parse,
                 self.m_fp_analysis_db, self.m_fp_setting_file, self.m_dp_db_out, is_rm)

    def on_close(self, event):
        main.on_c_parse_close()


class RationalizationService(RationalizationFrame):
    def on_pli_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "PLI解析",
                               "PLI_analysis_main_all_folder.py")
        checkSub(["cmd", "db", "dir", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_pli, self.m_fp_setting_file, self.m_dp_db_out)

    def on_close(self, event):
        main.on_rationalization_close()


class CobolService(CobolFrame):
    def on_cobol_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "COBOL解析",
                               "COBOL_analysis_main_all_folder.py")
        checkSub(["cmd", "db", "dir", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_analysis_db,
                 self.m_dp_cobol, self.m_fp_setting_file, self.m_dp_db_out)

    def on_close(self, event):
        main.on_cobol_close()


class NativePliService(NativePliFrame):
    def on_jcl_out_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "NativePLIソース整形ツール",
                               "native_pli_source_handler.py")
        checkSub(["cmd", "dir", "dir"], executeCmdStr, cmdPath, self.m_dp_input, self.m_dp_out)

    def on_close(self, event):
        main.on_native_pli_close()


class PliCmdService(PliCmdFrame):
    def on_jcl_out_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "MUTB_PLI呼出関係整理ツール",
                               "mutb_pli_cmd_handler.py")
        checkSub(["cmd", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_input, self.m_dp_out)

    def on_close(self, event):
        main.on_pli_cmd_close()


class PliService(PliFrame):
    def on_native_click(self, event):
        main.on_natvie_pli_click()

    # def on_pli_click(self, event):
    #     pass

    def on_rationalization_click(self, event):
        main.on_rationalization_click()

    def on_relationship_click(self, event):
        main.on_pli_cmd_click()

    def on_close(self, event):
        main.on_pli_close()


class PgmService(PgmFrame):
    def on_cobol_click(self, event):
        main.on_cobol_click()

    def on_pli_click(self, event):
        main.on_pli_click()

    def on_natural_click(self, event):
        main.on_natrual_click()

    def on_clist_click(self, event):
        main.on_clist_click()

    def on_c_parse_click(self, event):
        main.on_c_parse_click()

    def on_close(self, event):
        main.on_pgm_close()


class JclOutService(JclOutFrame):
    def on_jcl_out_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "JCL解析",
                               "make_JCLtoPROC.py")
        checkSub(["cmd", "db", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_analysis_db
                 , self.m_fp_setting_file, self.m_dp_excel_out)

    def on_close(self, event):
        main.on_jclout_close()


class MemberSplitService(MemberSplitFrame):
    def on_jcl_out_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "メンバー分割ツール",
                               "asset_member_handler.py")
        checkSub(["cmd", "dir", "dir"], executeCmdStr, cmdPath, self.m_dp_input, self.m_dp_out)

    def on_close(self, event):
        main.on_memberSplit_close()


class DataService(DataFrame):

    def on_result_click(self, event):
        main.on_result_click()

    def on_jcl_result_click(self, event):
        main.on_jcl_result_click()

    def on_cobol_result_click(self, event):
        main.on_cobol_result_click()

    def on_close(self, event):
        main.on_data_close()


class ResultService(ResultFrame):
    def on_result_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "data_organize_main.py")
        checkSub(["cmd", "dore", "dore", "excel", "bol"], executeCmdStr, cmdPath, self.m_fp_input
                 , self.m_fp_output, self.m_fp_setting_file, self.m_cb_is_db_clear.IsChecked())

    def on_close(self, event):
        main.on_result_close()


class JclResultService(JclResultFrame):
    def on_jcl_result_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "JCL解析",
                               "JCL_DB_merge.py")
        checkSub(["cmd", "dir", "dir"], executeCmdStr, cmdPath, self.m_dp_jcl_db
                 , self.m_fp_output)

    def on_close(self, event):
        main.on_jcl_result_close()


class CobolResultService(CobolResultFrame):
    def on_cobol_result_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "COBOL解析",
                               "COBOL_DB_merge.py")
        checkSub(["cmd", "dir", "dir", "bol"], executeCmdStr, cmdPath, self.m_dp_cobol_db
                 , self.m_fp_output, self.m_cb_is_call_output.IsChecked())

    def on_close(self, event):
        main.on_cobol_result_close()


class MachineDbService(MachineDbFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Client_DB_setup.py")
        checkSub(["cmd", "db", "dir", "bol"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_db_out
                 , self.m_cb_bol.IsChecked())

    def on_close(self, event):
        main.on_machine_db_close()


class PedDamService(PedDamFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "PED_DAM",
                               "PED_DAM_main_all_folder.py")
        checkSub(["cmd", "db", "dir", "dir", "dir"], executeCmdStr, cmdPath, self.m_fp_customer_db
                 , self.m_dp_out, self.m_dp_ped, self.m_dp_definition)

    def on_close(self, event):
        main.on_ped_dam_close()


class MachineBeforeService(MachineBeforeFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Applied_Analysis",
                               "Advance_analysis_main.py")
        checkSub(["cmd", "db", "dir"], executeCmdStr, cmdPath, self.m_fp_customer_db
                 , self.m_dp_out)

    def on_close(self, event):
        main.on_machine_before_close()


class OnlineReceiptService(OnlineReceiptFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Received_asset_setup.py")
        checkSub(["cmd", "db", "excel"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_out)

    def on_close(self, event):
        main.on_online_receipt_close()


class OnlineCustomerService(OnlineCustomerFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "All_Relations_setup.py")
        checkSub(["cmd", "db", "excel", "excel"], executeCmdStr, cmdPath, self.m_fp_customer_db
                 , self.m_dp_out, self.m_dp_maji)

    def on_close(self, event):
        main.on_online_customer_close()


class OnlineStartService(OnlineStartFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Starting_asset_split.py")
        checkSub(["cmd", "excel", "dir"], executeCmdStr, cmdPath, self.m_dp_setting, self.m_dp_out)

    def on_close(self, event):
        main.on_online_start_close()


class OnlineTestService(OnlineTestFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Test_Step_setup.py")
        checkSub(["cmd", "db", "excel"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_out)

    def on_close(self, event):
        main.on_online_test_close()


class OnlineAssetsService(OnlineAssetsFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "資産階層図",
                               "資産階層図3.py")
        checkSub(["cmd", "db", "dir", "bol"], executeCmdStr, cmdPath, self.m_fp_customer_db
                 , self.m_dp_out, self.m_cb_bol.IsChecked())

    def on_close(self, event):
        main.on_online_assets_close()


class OnlineRelatedService(OnlineRelatedFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "資産階層図",
                               "related_asset_output.py")
        checkSub(["cmd", "db", "dir"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_out)

    def on_close(self, event):
        main.on_online_related_close()


class StarumService(StarumFrame):
    def on_jcl_out_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "逆階層図ツール",
                               "callstratum.jar")
        checkSub(["cmd", "excel", "dir"], executeJavaCmdStr, cmdPath, self.m_fp_input, self.m_dp_out)

    def on_close(self, event):
        main.on_starum_close()


class MachineOnlineService(MachineOnlineFrame):
    def on_receipt_click(self, event):
        main.on_online_receipt_click()

    def on_customer_click(self, event):
        main.on_online_customer_click()

    def on_start_click(self, event):
        main.on_online_start_click()

    def on_test_click(self, event):
        main.on_online_test_click()

    def on_assets_click(self, event):
        main.on_online_assets_click()

    def on_stratum_click(self, event):
        main.on_starum_click()

    def on_related_click(self, event):
        main.on_online_related_click()

    def on_close(self, event):
        main.on_machine_online_close()


class BatchDataService(BatchDataFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Data_DSN_setup.py")
        checkSub(["cmd", "db", "excel"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_out)

    def on_close(self, event):
        main.on_batch_data_close()


class BatchStartService(BatchStartFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Starting_asset_split.py")
        checkSub(["cmd", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_setting, self.m_dp_out)

    def on_close(self, event):
        main.on_batch_start_close()


class BatchTestService(BatchTestFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Data_Organize",
                               "Test_Step_setup.py")
        checkSub(["cmd", "db", "excel"], executeCmdStr, cmdPath, self.m_fp_customer_db, self.m_dp_out)

    def on_close(self, event):
        main.on_batch_test_close()


class BatchOutService(BatchOutFrame):
    def on_analysis_click(self, event):
        cmdPath = os.path.join(os.getcwd(), "src", "Applied_Analysis_Source", "Batch_IO",
                               "Batch_IO_output.py")
        checkSub(["cmd", "db", "excel", "dir"], executeCmdStr, cmdPath, self.m_fp_customer_db
                 , self.m_fp_setting, self.m_dp_out)

    def on_close(self, event):
        main.on_batch_out_close()


class MachineBatchService(MachineBatchFrame):
    def on_data_click(self, event):
        main.on_batch_data_click()

    def on_start_click(self, event):
        main.on_batch_start_click()

    def on_test_click(self, event):
        main.on_batch_test_click()

    def on_batch_click(self, event):
        main.on_batch_out_click()

    def on_close(self, event):
        main.on_machine_batch_close()


class MachineService(MachineFrame):

    def on_db_click(self, event):
        main.on_machine_db_click()

    def on_ped_dam_click(self, event):
        main.on_ped_dam_click()

    def on_psb_click(self, event):
        event.Skip()

    def on_before_click(self, event):
        main.on_machine_before_click()

    def on_online_click(self, event):
        main.on_machine_online_click()

    def on_batch_click(self, event):
        main.on_machine_batch_click()

    def on_close(self, event):
        main.on_machine_close()


if __name__ == "__main__":
    app = wx.App()
    main = MainService(None)
    main.Show()
    app.MainLoop()
