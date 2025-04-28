from aiogram.fsm.state import State, StatesGroup

class DepositStates(StatesGroup):
    entering_amount = State()