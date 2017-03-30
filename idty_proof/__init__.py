PLUGIN_NAME = "Identity proof"
PLUGIN_VERSION = "0.1"
SAKIA_VERSION = "0.30.14"

from .controller import IdentityProofController


def plugin_exec(app, main_window):
    """
    :param sakia.app.Application app:
    :param sakia.gui.main_window.controller.MainWindowController main_window:
    """
    from PyQt5.QtWidgets import QAction
    tool_menu = main_window.toolbar.view.toolbutton_menu.menu()
    action_publish_proof = QAction("Publish an identity proof", tool_menu)
    tool_menu.addAction(action_publish_proof)
    action_publish_proof.triggered.connect(lambda a=app, mw=main_window: open_dialog(a, mw))

def open_dialog(app, main_window):
    """
    :param sakia.app.Application app:
    :param sakia.gui.main_window.controller.MainWindowController main_window:
    """
    current_connection = main_window.navigation.model.current_connection()
    IdentityProofController.open_dialog(None, app, current_connection)

