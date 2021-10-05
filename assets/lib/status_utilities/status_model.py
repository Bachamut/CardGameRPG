from assets.lib.status_utilities.status_manager import StatusManager


class StatusType:

    def __init__(self, status_type):

        config = StatusManager.status_config

        for key, value in config.items():
            if key == status_type:

                self.status_type = value['status_type']
                self.name = value['name']
                self.description = value['description']
                self.persistance = value['persistance']
                self.status_role = value['status_role']
                self.rate = value['rate']
                self.activation = value['activation']
                self.deactivation = value['deactivation']

class Status(StatusType):

    def __init__(self, status_type, value, duration):
        super(Status, self).__init__(status_type)

        self.value = value
        self.duration = duration
        self.source = None