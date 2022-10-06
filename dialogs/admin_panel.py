from aiogram_dialog import Dialog

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Checkbox, Button
from aiogram_dialog.widgets.text import Const

from handlers.users.admin_panel import bool_settings, button_settings, set_text_ad
from loader import registry
from states.admin_panel import StatesAP
from utils.dbworker import get_settings


async def settings_dialog():
    settings = await get_settings()
    window_settings = []

    for k, v in settings.items():
        if v['type'] == 'bool':
            window_settings.append(
                Checkbox(
                    Const(f"✓  {v['view_name']}"),
                    Const(f" {v['view_name']}"),
                    id=k,
                    default=v['value'],
                    on_state_changed=bool_settings,
                )
            )
        elif v['type'] == 'text':
            window_settings.append(
                Button(
                    Const(f"{v['view_name']}"),
                    id=k,
                    on_click=button_settings
                )
            )

    registry.register(
        Dialog(
            Window(
                Const("Настройки:"),
                *window_settings,
                Button(
                    Const("Закрыть меню"),
                    id='delete',
                    on_click='delete'
                ),
                state=StatesAP.start
            ),
            Window(
                Const("Введи текст:"),
                MessageInput(set_text_ad),
                state=StatesAP.set_text
            )
        )
    )