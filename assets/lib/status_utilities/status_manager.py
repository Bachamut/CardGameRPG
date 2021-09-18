import json

from assets.lib.battle_system.status import StatusType, Status


class StatusManager:

    status_config = dict()
    status_type_list = list()

    @staticmethod
    def load_config(filename):

        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                StatusManager.status_config.update({key: value})

    @staticmethod
    def create_status_types():

        config = StatusManager.status_config

        for key, value in config.items():

            status_type = StatusType()

            status_type.status_id = value['status_id']
            status_type.name = value['name']
            status_type.description = value['description']
            status_type.persistance = value['persistance']
            status_type.activation = value['activation']

            StatusManager.status_type_list.append(status_type)

    @staticmethod
    def create_status(key):

        config = StatusManager.status_config[key]
        status = Status()

        status.status_type = config['status_type']
        status.value = config['value']
        status.duration = config['duration']

        return status


