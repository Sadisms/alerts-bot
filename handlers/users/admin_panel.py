from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram_dialog import ChatEvent, DialogManager, StartMode, Dialog
from aiogram_dialog.widgets.kbd import ManagedCheckboxAdapter, Button

from keyboards.admin_panel import admin_panel_keyboards
from loader import dp, bot
from states.admin_panel import StatesAP
from utils.dbworker import set_settings_value
from utils.files_helper import add_file, get_files_answer, get_files_dict, delete_file
from utils.tg_helper import get_logs_archive, get_excel_users


@dp.message_handler(CommandStart(), is_admin=True, state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        text=f'Hello, {message.from_user.full_name}',
        reply_markup=admin_panel_keyboards()
    )


@dp.callback_query_handler(text='add_files')
async def get_files_start(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer(
        text='Отправь файл:'
    )
    await StatesAP.get_file.set()


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=StatesAP.get_file)
async def get_files(message: types.Message, state: FSMContext):
    attach = message.document
    file_name = attach.file_name

    file_info = await bot.get_file(attach.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    await add_file(
        file_name=file_name,
        content=downloaded_file.getvalue()
    )

    await state.finish()

    await message.answer(
        text=f'Файл {file_name} добавлен'
    )


@dp.callback_query_handler(text='delete_file')
async def delete_file_start(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if file_table := get_files_answer():
        await callback_query.message.answer(
            text=f'Файлы:\n{file_table}',
            parse_mode='HTML'
        )
        await callback_query.message.answer(
            text='Введи ID файла:'
        )
        await StatesAP.delete_file.set()

    else:
        await callback_query.message.answer(
            text='Файлов нет'
        )


@dp.message_handler(state=StatesAP.delete_file)
async def delete_file_end(message: types.Message, state: FSMContext):
    file_id = message.text
    files = get_files_dict()

    if not file_id.isdigit():
        await message.answer(
            text='Неверно указан ID файла!'
        )
        return

    elif int(file_id) not in files:
        await message.answer(
            text='Файла с таким ID нет!'
        )
        return

    await state.finish()

    file_id = int(file_id)
    file_name = files[file_id]
    delete_file(file_name)

    await message.answer(
        text=f'Файл {file_name} удалён'
    )


@dp.callback_query_handler(text='get_data_users')
async def get_data_users(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    if document := await get_excel_users():
        await callback_query.message.answer_document(
            document
        )


@dp.callback_query_handler(text='get_logs')
async def get_logs(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer_document(
        get_logs_archive()
    )


@dp.callback_query_handler(text='delete')
async def delete_message(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


# ------------------------------------------------------
# DIALOG                                               #
# ------------------------------------------------------


@dp.callback_query_handler(text='settings')
async def settings_start(callback_query: types.CallbackQuery, dialog_manager: DialogManager):
    await callback_query.message.delete()
    await dialog_manager.start(StatesAP.start, mode=StartMode.RESET_STACK)


async def bool_settings(
        event: ChatEvent,
        checkbox: ManagedCheckboxAdapter,
        manager: DialogManager
):
    value = checkbox.is_checked()
    key = checkbox.widget.widget_id

    await set_settings_value(
        key=key,
        value=value,
        type_value='bool'
    )

    checkbox.widget.default = checkbox.is_checked()

    await event.message.answer(
        text='Значение установлено.'
    )

    await manager.done()


async def button_settings(
        callback_query: types.CallbackQuery,
        button: Button,
        manager: DialogManager
):
    manager.current_context().dialog_data['key'] = button.widget_id
    await manager.switch_to(StatesAP.set_text)


async def set_text_ad(message: types.Message, dialog: Dialog, manager: DialogManager):
    value = message.text
    key = manager.current_context().dialog_data['key']

    await set_settings_value(
        key=key,
        value=value,
        type_value='text'
    )

    await message.answer(
        text='Значение установлено.'
    )

    await manager.done()
