from PyQt5.QtWidgets import QDialog
from .idity_proof_uic import Ui_IdentityProofDialog
from sakia.gui.widgets import toast
from sakia.gui.widgets.dialogs import QAsyncMessageBox
from sakia.constants import ROOT_SERVERS
from duniterpy.documents import Identity, MalformedDocumentError
from enum import Enum


class IdentityProofView(QDialog, Ui_IdentityProofDialog):
    """
    The view of the certification component
    """

    def __init__(self, parent, search_user_view, user_information_view, password_input_view):
        """

        :param parent:
        :param sakia.gui.search_user.view.SearchUserView search_user_view:
        :param sakia.gui.user_information.view.UserInformationView user_information_view:
        :param list[sakia.data.entities.Connection] connections:
        """
        super().__init__(parent)
        self.setupUi(self)

    def set_keys(self, connections):
        self.combo_connection.clear()
        for c in connections:
            self.combo_connection.addItem(c.title())

    def set_selected_key(self, connection):
        """
        :param sakia.data.entities.Connection connection:
        """
        self.combo_connection.setCurrentText(connection.title())

    def set_label_confirm(self, currency):
        self.label_confirm.setTextFormat(Qt.RichText)
        self.label_confirm.setText("""<b>Vous confirmez engager votre responsabilité envers la communauté Duniter {:}
    et acceptez de certifier le compte Duniter {:} ci-dessus.<br/><br/>
Pour confirmer votre certification veuillez confirmer votre signature :</b>""".format(ROOT_SERVERS[currency]["display"],
                                                                                     ROOT_SERVERS[currency]["display"]))

    async def show_success(self, notification):
        text = (self.tr("Identity proof"),
                          self.tr("Success sending identity proof"))
        if notification:
            toast.display(*text)
        else:
            await QAsyncMessageBox.information(self, *text)

    async def show_error(self, notification, error_txt):
        text = (self.tr("Certification"), self.tr("Could not broadcast certification : {0}"
                                                            .format(error_txt)))
        if notification:
            toast.display(*text)
        else:
            await QAsyncMessageBox.critical(self, *text)
