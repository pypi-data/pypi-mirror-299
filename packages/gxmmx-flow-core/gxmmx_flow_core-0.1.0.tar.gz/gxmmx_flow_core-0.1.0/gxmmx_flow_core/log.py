# ------------------------------------------------------------------------------
# Flow Log
# ------------------------------------------------------------------------------


class FlowLog:

    @staticmethod
    def err(msg: str, should_exit: bool = True):
        print(f"\033[91m{msg}\033[0m")
        if should_exit:
            exit(1)

    @staticmethod
    def wrn(msg: str):
        print(f"\033[93m{msg}\033[0m")

    @staticmethod
    def ok(msg: str):
        print(f"\033[92m{msg}\033[0m")

    @staticmethod
    def msg(msg: str):
        print(f"{msg}")
