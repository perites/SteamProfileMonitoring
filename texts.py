texts = {
    "game_bought_user": "О, купив нарешті, сподіваюсь все інше вже допройшов, щоб як тільки я приїду ОДРАЗУ Ж пішли 😈",
    "game_bought_admin": "ПЕРЕМОГА БУДЕ, купив купив купив",
    "game_bought_dchannel": "ПЕРЕМОГА БУДЕ, <@{}> купив секіро",

    "sale_ends_soon_user": "Скоро кінець літнього розпродажу ( менш ніж за 24 години ), а ти ще не купив Cекіро, так не піде.\nОзнайомтесь: https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/",
    "sale_ends_soon_admin": "кінець розпродажу за 24 години а він ще не купив, нагадування надіслано",
    "sale_ends_soon_dchannel": "Літній розпродаж закінчується менш ніж за 24 години, саме час купувати все що відкладали (<@{}>)",

    "sale_ended_user": "Літній розпродаж,закінчився, а ти ще не купив секіро, це зрада.\nНу що ж, тепер прийдеться купити за 2к 😈\nhttps://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/",
    "sale_ended_admin": "розпродаж закінчився а він ще не купив, пахне зрадою , нагадування надіслано",
    "sale_ended_dchannel": "Літній розпродаж закінчився, а хтось (<@{}>) так і не купив що мав купити",

    "counter_message_admin": "Ні, ще не купив ("
}


def get_text(text_name, *args, **kwargs):
    return texts[text_name].format(*args, **kwargs)
