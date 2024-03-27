

from runtime.ast import Program
from runtime.runtime import Context, Runtime

class ProgrameRuntime(Runtime):
    
    def exec(self, program: Program):
        result = program.exec(self)
        return result

    def show_values(self):
        self.context.show_values()

    def set_value(self, name, value):
        self.context.set_value(name, value)
