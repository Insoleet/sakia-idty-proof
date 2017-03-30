from PyQt5.QtCore import QObject
from sakia.data.processors import IdentitiesProcessor, CertificationsProcessor, \
    BlockchainProcessor, ConnectionsProcessor
import attr


class IdentityProofModel(QObject):
    """
    The model of Certification component
    """

    def __init__(self, app, connection):
        super().__init__()
        self.app = app
        self.connection = connection
        self._connections_processor = ConnectionsProcessor.instanciate(self.app)
        self._identities_processor = IdentitiesProcessor.instanciate(self.app)
        self._blockchain_processor = BlockchainProcessor.instanciate(self.app)

    def change_connection(self, index):
        """
        Change current currency
        :param int index: index of the community in the account list
        """
        self.connection = self.connections_repo.get_currencies()[index]

    def available_connections(self):
        return self._connections_processor.connections_with_uids()

    def set_connection(self,  index):
        connections = self._connections_processor.connections_with_uids()
        self.connection = connections[index]

    def notification(self):
        return self.app.parameters.notifications
