class Action:
    """
    One skill use
    """
    def __init__(self, use_dict: dict):
        self.use_dict: dict = use_dict

    def set_dict(self, use_dict: dict):
        self.use_dict = use_dict
