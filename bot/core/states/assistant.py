from aiogram.fsm.state import StatesGroup, State

class Assistant(StatesGroup): 
    default = State()
    task_manager = State()
    edit_task = State()
    search_tasks = State()
    google_oauth = State()
    