#from BaseModel import BaseModel
from ..BaseModel.BaseModel import BaseModel
from typing import Callable, Optional, DefaultDict, Dict, Any
from collections import defaultdict
from ..Input import IInput
#from IController import IController
from mymvc.BaseController.IController import IController

class BaseController:
    def __init__(self, input_handler: IInput) -> None:
        self._input_handler = input_handler
        self._running = True
        self.controllers = {}  # Словарь для хранения контроллеров
        self.current_controller: IController = None
        self.models: Dict = {}  # Словарь для хранения моделей

    def start_cycle(self) -> None:
        while self._running:
            key = self._input_handler.get_key()
            if key is not None:
                updated_data = self.handle_key(key)
                if updated_data:
                    self.update_models(updated_data)

    def handle_key(self, key: int) -> str:
        """
        Обрабатывает клавишу в зависимости от текущего активного контроллера.
        :param key: Код нажатой клавиши
        :return: Результат выполнения команды
        """
        if self.current_controller:
            return self.current_controller.handle_key(key)
        else:
            return "Нет активного контроллера."
    
    def add_controller(self, mode: str, controller: IController) -> None:
        """
        Добавляет контроллер в систему.
        :param mode: Название режима (например, 'navigation', 'input', и т.д.)
        :param controller: Контроллер, реализующий интерфейс IController
        """
        self.controllers[mode] = controller
        controller.register_commands()
    
    def add_model(self, name: str, model: BaseModel) -> None:
        """
        Добавляет модель в словарь моделей.
        :param name: Уникальное имя модели.
        :param model: Экземпляр модели.
        """
        self.models[name] = model

    def get_model(self, name: str):
        """
        Возвращает модель по имени.
        :param name: Имя модели.
        :return: Экземпляр модели или None, если модель не найдена.
        """
        return self.models.get(name)

    def update_models(self, data: Dict[str, Any]) -> None:
        """
        Обновляет все указанные модели, используя предоставленные данные.
        :param data: Словарь с обновлениями для каждой модели.
                    Формат: {
                        'model': [список моделей],
                        'update': {
                            обновление для каждой модели
                        }
                    }
        """
        models_to_update = data.get('model', [])
        updates = data.get('update', {})

        if not isinstance(models_to_update, list):
            raise ValueError("'model' должен быть списком.")

        for model_name in models_to_update:
            if model_name in self.models:
                update_data = updates.get(f'update_{model_name}', {})
                if update_data:
                    self.models[model_name].update_data(update_data)
                else:
                    print(f"Нет обновлений для модели: {model_name}")
            else:
                print(f"Модель {model_name} не найдена.")
    
    def switch_controller(self, mode: str) -> None:
        """
        Переключает текущий контроллер в зависимости от переданного режима.
        :param mode: Название режима
        """
        if mode in self.controllers:
            self.current_controller = self.controllers[mode]
        else:
            raise ValueError(f"Неизвестный режим: {mode}")