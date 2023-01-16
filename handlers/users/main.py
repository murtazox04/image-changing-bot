import asyncio
from io import BytesIO

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from decouple import config

from loader import dp, bot
from states.main_state import GetState


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}! Please send audio...")


@dp.message_handler(content_types=['audio'], state=None)
async def get_music(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        audio_id = message.audio.file_id
        performer = message.audio.performer
        audio_title = message.audio.title
        file_name = message.audio.file_name
        data['audio_id'] = audio_id
        data['performer'] = performer
        data['audio_title'] = audio_title
        data['file_name'] = file_name

        await message.answer("Okay! Please send the photo you want to add to the audio...")
    await GetState.photo.set()


@dp.message_handler(content_types=['photo'], state=GetState.photo)
async def send_audio_with_thumb(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        audio_id = data['audio_id']
        audio_title = data['audio_title']
        file_name = data['file_name']
        performer = data['performer']
        image_id = message.photo[-1].file_id

        download_audio = await bot.download_file_by_id(audio_id)
        download_image = await bot.download_file_by_id(image_id)

        image = types.InputFile(download_image)
        audio = types.InputFile(download_audio, filename=f"{file_name}.mp3")

        download_image.seek(0)
        download_audio.seek(0)

        await message.reply("I am sending you the audio...")
        await bot.send_audio(
            chat_id=message.from_user.id, audio=audio, thumb=image, performer=performer, title=audio_title
        )
    await state.finish()
