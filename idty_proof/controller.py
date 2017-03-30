import asyncio

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from sakia.decorators import asyncify
from sakia.gui.sub.password_input import PasswordInputController
from sakia.gui.widgets import dialogs
from .model import IdentityProofModel
from .view import IdentityProofView
import attr


class IdentityProofController(QObject):
    """
    The identity proof controller
    """
    def __init__(self, view, model, password_input):
        super().__init__()
        self.view = view
        self.model = model
        self.password_input = password_input
        self.view.button_box.accepted.connect(self.accept)
        self.view.button_box.rejected.connect(self.reject)
        self.view.combo_connection.currentIndexChanged.connect(self.change_connection)

    @classmethod
    def create(cls, parent, app):
        """
        Instanciate a Certification component
        :param sakia.gui.component.controller.ComponentController parent:
        :param sakia.app.Application app: sakia application
        :return: a new Certification controller
        :rtype: CertificationController
        """
        password_input = PasswordInputController.create(None, None)

        view = IdentityProofView(parent.view if parent else None, password_input.view)
        model = IdentityProofModel(app)
        view.set_label_confirm(app.currency)
        identity_proof = cls(view, model, password_input)

        view.set_keys(identity_proof.model.available_connections())
        return identity_proof

    @classmethod
    def open_dialog(cls, parent, app, connection):
        """
        Certify and identity
        :param sakia.gui.component.controller.ComponentController parent: the parent
        :param sakia.core.Application app: the application
        :param sakia.core.Account account: the account certifying the identity
        :param sakia.core.Community community: the community
        :return:
        """
        dialog = cls.create(parent, app)
        dialog.set_connection(connection)
        dialog.refresh()
        return dialog.exec()

    def change_connection(self, index):
        self.model.set_connection(index)
        self.password_input.set_connection(self.model.connection)
        self.refresh()

    def set_connection(self, connection):
        if connection:
            self.view.combo_connection.setCurrentText(connection.title())
            self.password_input.set_connection(connection)

    @asyncify
    async def accept(self):
        """
        Validate the dialog
        """

        if not self.user_information.model.identity.member:
            result = await dialogs.QAsyncMessageBox.question(self.view, self.tr("Publishing an identity proof"),
"""
Please ensure that the informations entered are correct.</br>
No change will be possible once published.
These informations will be cyphered and published on the blockchain.""")
            if result == dialogs.QMessageBox.No:
                return

        self.view.button_box.setDisabled(True)
        secret_key, password = self.password_input.get_salt_password()
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if result[0]:
            QApplication.restoreOverrideCursor()
            await self.view.show_success(self.model.notification())
            self.view.accept()
        else:
            await self.view.show_error(self.model.notification(), result[1])
            QApplication.restoreOverrideCursor()
            self.view.button_box.setEnabled(True)

    @asyncify
    async def reject(self):
        self.view.reject()

    def async_exec(self):
        future = asyncio.Future()
        self.view.finished.connect(lambda r: future.set_result(r))
        self.view.open()
        self.refresh()
        return future

    def exec(self):
        self.refresh()
        self.view.exec()
