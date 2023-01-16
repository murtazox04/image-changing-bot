from aiogram import executor
from loader import dp
import middlewares, handlers, states


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
