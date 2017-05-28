from datetime import datetime


class Utility(object):
    time_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def get_field_recursively(field_list, data):
        for field in field_list:
            if field in data:
                data = data[field]
            else:
                break
        return data

    @staticmethod
    def get_current_time():
        # Return the current time stamp in milliseconds.
        return str(datetime.now())[:-4]

