import sys

class JongaInterceptor:
    def __init__(self):
        self.captured_output = []

    def write(self, message):
        self.captured_output.append(message)
        sys.__stdout__.write("jonga careca")

    def flush(self):
        pass

sys.stdout = JongaInterceptor()
