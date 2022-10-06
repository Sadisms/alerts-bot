from aiogram import types


def admin_panel_keyboards():
    menu_ap = types.InlineKeyboardMarkup(row_width=1)
    menu_ap.add(
        types.InlineKeyboardButton(
            text='Настройки',
            callback_data='settings'
        ),
        types.InlineKeyboardButton(
            text='Запросить логи',
            callback_data='get_logs'
        ),
        types.InlineKeyboardButton(
            text='Добавить файл',
            callback_data='add_files'
        ),
        types.InlineKeyboardButton(
            text='Удалить файл',
            callback_data='delete_file'
        ),
        types.InlineKeyboardButton(
            text='Получить данные о пользователях',
            callback_data='get_data_users'
        ),
        types.InlineKeyboardButton(
            text='Закрыть меню',
            callback_data='delete'
        ),
    )
    return menu_ap
