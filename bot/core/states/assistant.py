from aiogram.fsm.state import StatesGroup, State

class Assistant(StatesGroup): 
    default = State()
    task_manager = State()