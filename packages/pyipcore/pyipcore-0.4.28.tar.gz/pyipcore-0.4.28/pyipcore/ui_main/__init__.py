import os.path
import time
from pyipcore.ui_main.ui_main import Ui_MainForm
from pyipcore.ui_main.ui_style import UiTool_StyleAdjust
from pyipcore.ipcore import IpCore, IpCoreCompileError, VAR_PARAM_TYPE, VAR_PORT_TYPE
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget, QMainWindow, QLineEdit, QCheckBox, QHBoxLayout
from pyipcore.ui_main.creator_page.ipc_creator import QIpCoreCreator
from pyipcore.ui_utils import *
from pyipcore.ipc_utils import *
from pyipcore.ip_module_view import IpCoreView
from qwork.utils import QSetting
from files3 import files
from pyverilog.vparser.parser import ParseError


class TaskWorker(QThread):
    """
    一个Worker线程，用于处理InstCode的生成。
    具体来说，它会在一个循环中，每隔dt时间，从任务队列中取出一个任务并执行。
    而任务队列中的任务目前可以理解为一个InstCode生成函数。
    """

    def __init__(self, dt=0.2):
        super().__init__()
        self._tasks = []
        self._args = []
        self._flag = True
        self._dt = dt


    def run(self):
        while self._flag:
            if len(self._tasks) > 0:
                task = self._tasks.pop(0)
                args = self._args.pop(0)
                try:
                    _ = task(*args)
                except Exception as e:
                    print(f"Error: {e.__class__.__name__}: {str(e)}")


            time.sleep(self._dt)

    def add(self, task, *args):
        self._tasks.append(task)
        self._args.append(args)

    def stop(self):
        self._flag = False

    def __bool__(self):
        return self._flag

    def __len__(self):
        return len(self._tasks)


class QInspectorContainer(QWidget):
    def __init__(self, callback, parent=None):
        super(QInspectorContainer, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self._callback = callback
        self._current:QMonoInspector = None
        self._logo = QMonoLogo()
        self._layout.addWidget(self._logo)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        # 移除先前组件
        if self._current is not None:
            self._layout.removeWidget(self._current)
            del self._current
        else:
            self._layout.removeWidget(self._logo)

        # 赋值为新组件
        self._current = value
        if self._current is not None:
            self._current.paramChanged.connect(self._callback)
            self._layout.addWidget(self._current)
        else:
            self._layout.addWidget(self._logo)


WORKER_ACTIVE_DELTA = 1.0
WORKER_DEACTIVE_DELTA = 3.0
class GUI_Main(QMainWindow):
    onOpen = pyqtSignal(str)  # dir_path.   xxx.ipc  # is a dir
    onClose = pyqtSignal()      # close file, no args
    onExport = pyqtSignal(str)  # dir_path  # export to this target
    def __init__(self):
        super(GUI_Main, self).__init__()
        self.qst = QSetting()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self._render_lock = False
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.load_current_size()
        self.ui.tab_sc.setCurrentIndex(0)

        # 自身的独立UI
        self.initUI()

        # add VarItemWidget into var_layout
        self.var_widget = QInspectorContainer(self._enable_ipcore_generate_update)
        self._need_update_flag = False

        self.ui.gbox_var.layout().addWidget(self.var_widget)

        # close即退出
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        # worker
        self.worker = TaskWorker()
        self.worker.start()
        self.worker.dt = WORKER_DEACTIVE_DELTA

        # vars
        self.ipcore:IpCore = None
        self.ip_creator = None
        self.var_dict = {}

        # /// customs
        # \t = 4 spaces
        self.ui.ptxt_rc.setTabStopWidth(4 * 4)
        self.ui.ptxt_cc.setTabStopWidth(4 * 4)
        self.ui.ptxt_ic.setTabStopWidth(4 * 4)
        self.reset_signals()

        # reset ptxt to QVerilogEdit
        self.reset_ptxt_xcs()

        # style change
        UiTool_StyleAdjust.effect(self.ui)


    @property
    def debug(self):
        return self.ui.action_debug.isChecked()

    @property
    def params(self):
        return self.var_widget.current.params

    def reset_signals(self):
        """
        重新绑定信号槽
        :return:
        """
        self.ui.action_file_open.triggered.connect(self.open_file)
        self.ui.action_file_close.triggered.connect(self.close_file)
        self.ui.action_file_scs.triggered.connect(self.save_current_size)
        self.ui.action_file_quit.triggered.connect(self.close)
        self.ui.action_proj_export.triggered.connect(self.export_proj)
        self.ui.action_help_readme.triggered.connect(lambda: PopInfo("Readme", "请参考README.md"))
        self.ui.action_help_about.triggered.connect(self.show_about)
        self.ui.tab_main.currentChanged.connect(self._fit_module_view)

        # ---
        self.onOpen.connect(self._on_open)
        self.onClose.connect(self._on_close)
        self.onExport.connect(self._on_export)

    def _fit_module_view(self, index):
        tab = self.ui.tab_main.widget(index)
        if tab is self.ui.tab_main_body:
            self.ui.ptxt_mv.scale_tofit()

    def reset_ptxt_xcs(self):
        """
        重置代码显示区域为VerilogEditor
        """
        self.ui.horizontalLayout_3.removeWidget(self.ui.ptxt_rc)
        self.ui.ptxt_rc = QVerilogEdit(self.ui.tab_rc)
        self.ui.ptxt_rc.setReadOnly(True)
        self.ui.ptxt_rc.setObjectName("ptxt_rc")
        self.ui.horizontalLayout_3.addWidget(self.ui.ptxt_rc)
        self.ui.horizontalLayout_4.removeWidget(self.ui.ptxt_cc)
        self.ui.ptxt_cc = QVerilogEdit(self.ui.tab_cc)
        self.ui.ptxt_cc.setReadOnly(True)
        self.ui.ptxt_cc.setObjectName("ptxt_cc")
        self.ui.horizontalLayout_4.addWidget(self.ui.ptxt_cc)
        self.ui.horizontalLayout_5.removeWidget(self.ui.ptxt_ic)
        self.ui.ptxt_ic = QVerilogEdit(self.ui.tab_ic)
        self.ui.ptxt_ic.setReadOnly(True)
        self.ui.ptxt_ic.setObjectName("ptxt_ic")
        self.ui.horizontalLayout_5.addWidget(self.ui.ptxt_ic)
        self.ui.horizontalLayout_2.removeWidget(self.ui.ptxt_mv)
        self.ui.ptxt_mv = IpCoreView(self.ui.tab_mv)
        self.ui.horizontalLayout_2.addWidget(self.ui.ptxt_mv)


    def initUI(self):
        layout = self.ui.tab_main_creator.layout()
        layout.setContentsMargins(4, 0, 0, 0)
        layout.setSpacing(0)
        self.core_widget__ipc_creator = QIpCoreCreator()
        self.core_widget__ipc_creator.compileIpcEvent.connect(self.compile_handler)
        layout.addWidget(self.core_widget__ipc_creator)

    def compile_handler(self,
                        name, author, brand, model, board, group,
                        fmain, ficon, freadme, fmanual,
                        subfiles, otherpaths):
        # 假设name不为空
        try:
            res = IpCore.Compile(
                name, author, brand, model, board, group,
                fmain, ficon, freadme, fmanual,
                subfiles, otherpaths
            )
        except IpCoreCompileError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        # 询问save路径
        f = files(type='.perfer')
        fdir = f['last_export_dir']
        fdir = os.path.abspath(fdir) if fdir and os.path.isdir(fdir) else os.getcwd()
        fdir = QFileDialog.getExistingDirectory(self, "选择导出路径", fdir)
        if not fdir:
            return
        if not os.path.isdir(fdir):
            PopError("错误", f"路径无效: {fdir}")
            return

        # 保存
        f.last_export_dir = fdir
        groups = parse_group_path(group)
        if groups:
            fdir = os.path.join(fdir, *groups)
            if not os.path.exists(fdir):
                os.makedirs(fdir)
        fipc = files(fdir, IPC_SUFFIX)
        for k, v in res.items():
            fipc[name, k] = v
        PopInfo("Info", "编译导出成功.")
        try:
            set_ipcdir_icon(os.path.join(fdir, name + IPC_SUFFIX))
        except ThirdToolFolderIcoNotFound as e:
            PopWarn("工具未下载", str(e), 1.5)
            return
        except FolderIcoPathContainSpace as e:
            PopWarn("路径包含空格", str(e))
            return
        except Exception as e:
            PopWarn("警告", f"设置图标失败: {e}\n*该功能不影响使用，但可能导致图标显示不正常.")
            return


    def _enable_ipcore_generate_update(self, *args):
        if not len(self.worker):
            self.worker.add(self._enter_update_vars)

    def _enter_update_vars(self, *args, default=False):
        # update cc ic
        try:
            if default:
                self.ipcore.build()
            else:
                self.ipcore.build(**self.params)
        except Exception as e:
            error = f"{e.__class__.__name__}:\n{str(e)}"
            self.ui.ptxt_cc.setText(error)
            self.ui.ptxt_ic.setText(error)
            self.ui.ptxt_mv.render_error(error)
            return
        # print("finish build")
        self.ui.ptxt_cc.setText(self.ipcore.built)
        self.ui.ptxt_ic.setText(self.ipcore.icode)
        self.ui.ptxt_mv.render_ipcore(self.ipcore)
        # update inspector
        if self.var_widget.current is not None:
            self.var_widget.current.rebuildTrigger.emit(self.ipcore._mono)


    def open_file(self):
        # open a directory
        path = self.qst.getExistingDirectory(f"选择IP核:({IPC_SUFFIX})", stlast=True)
        if not path: return
        if not os.path.isdir(path):
            PopError("错误", "路径无效")
            return
        self.onOpen.emit(path)

    def _on_open(self, path):
        fdir, fnametype = os.path.split(path)
        fname = fnametype[:-len(IPC_SUFFIX)]
        f = files(fdir, IPC_SUFFIX)
        if not f.has(fname):
            PopError("错误", "IPC文件不存在或无法读取")
            return

        self.ipcore = IpCore(fdir, fname)
        self.ui.ptxt_rc.setText(self.ipcore.content)
        self.ui.ptxt_cc.setText("")
        self.ui.ptxt_ic.setText("")
        self.ui.tab_sc.setCurrentIndex(0)
        self._enter_update_vars(default=True)

        # model
        try:
            self.var_widget.current = self.ipcore.GetInspector(skip_update=True)
        except Exception as e:
            PopError(f"{e.__class__.__name__}:", str(e), 1.5)
            return

        # active worker
        self.worker.dt = WORKER_ACTIVE_DELTA

        PopInfo("Info", "打开成功.")

    def close_file(self):
        self.onClose.emit()

    def _on_close(self):
        self.ipcore = None
        self.ui.ptxt_rc.setText("")
        self.ui.ptxt_cc.setText("")
        self.ui.ptxt_ic.setText("")
        self.ui.ptxt_mv.clear()
        self.var_widget.current = None
        self.ui.tab_sc.setCurrentIndex(0)

        # deactive worker
        self.worker.dt = WORKER_DEACTIVE_DELTA


    def save_current_size(self):
        f = files(os.getcwd(), '.prefer')
        f["window_size"] = self.size()


    def load_current_size(self):
        f = files(os.getcwd(), '.prefer')
        size = f["window_size"]
        if size:
            self.resize(size)

    def export_proj(self):
        if self.ipcore is None:
            PopWarn("警告", "请先打开一个IP核文件.")
            return
        path = self.qst.getSaveFileName("选择导出的verilog文件", "", VERILOG_TYPE, filename=self.ipcore.name)[0]
        if not path: return
        self.onExport.emit(path)


    def _on_export(self, path:str):
        fname = os.path.basename(path)
        dirname = os.path.dirname(path)
        try:
            try:
                self.ipcore.export(dirname, spec_name=fname)
            except FileExistsError as e:
                if QMessageBox.question(self, "Warning", f"Do you want to overwrite it?\n\nexists: {e}",
                                        QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    self.ipcore.export(dirname, spec_name=fname, overwrite=True)
                else:
                    return
        except Exception as e:
            PopError(f"{e.__class__.__name__}:", str(e), 1.5)
            return
        PopInfo("Info", "导出成功.")


    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gui = GUI_Main()
    gui.show()
    sys.exit(app.exec_())
