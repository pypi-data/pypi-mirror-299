# ------------------------------------------------------------------------------
# Flow Errors
# ------------------------------------------------------------------------------


class FlowError(Exception):
    def __init__(self, msg: str):
        """
        ### FlowError

        Flow base error.
        All Flow sub errors parent this one. Should not be called directly.
        """
        super().__init__(f"Flow Error: {msg}")


class FlowConfigError(FlowError):
    def __init__(self, msg: str):
        super(FlowError, self).__init__(f"Flow Config Error: {msg}")


class FlowValidationError(FlowError):
    def __init__(self, msg: str):
        super(FlowError, self).__init__(f"Flow Config Error: {msg}")


class FlowCodeQualityError(FlowError):
    def __init__(self, msg: str):
        super(FlowError, self).__init__(f"Flow CodeQuality Error: {msg}")
