
from aiogram.fsm.state import State, StatesGroup

class BetStates(StatesGroup):
    choosing_match = State()
    entering_amount = State()
    choosing_team = State()
    top_up_balance = State()
