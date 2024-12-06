from ..BaseController.IController import IController

class ICommand:
    def execute(self, controller: IController) -> str:
        pass
