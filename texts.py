from dataclasses import dataclass


@dataclass
class EventTexts:
    text_for_user: str or None
    text_for_admin: str or None
    text_for_dchannel: str or None

    need_format: list[str] or None

    def format(self, *f_args, **f_kwargs):
        if self.need_format:
            for name in self.need_format:
                self.__dict__[name] = self.__dict__[name].format(*f_args, **f_kwargs)

        return self

    def get_texts(self):
        texts = {}
        for name, value in self.__dict__.items():
            if name.startswith("text_for") and value:
                texts[name] = value

        return texts


game_bought = EventTexts(
    text_for_user="О, купив нарешті, сподіваюсь все інше вже допройшов, щоб як тільки я приїду ОДРАЗУ Ж пішли 😈",

    text_for_admin="ПЕРЕМОГА БУДЕ, купив купив купив",

    text_for_dchannel="ПЕРЕМОГА БУДЕ, <@{}> купив секіро",

    need_format=['text_for_dchannel']
)

sale_ends_soon = EventTexts(
    text_for_user='Скоро кінець літнього розпродажу ( менш ніж за 24 години ), а ти ще не купив Cекіро, так не піде.\n Ознайомтесь: https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/',

    text_for_admin="кінець розпродажу за 24 години а він ще не купив, нагадування надіслано",

    text_for_dchannel="Літній розпродаж закінчується менш ніж за 24 години, саме час купувати все що відкладали (<@{}>)",

    need_format=['text_for_dchannel']

)

sale_ended = EventTexts(
    text_for_user='Літній розпродаж,закінчився, а ти ще не купив секіро, це зрада.\nНу що ж, тепер прийдеться купити за 2к 😈\nhttps://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/',

    text_for_admin="розпродаж закінчився а він ще не купив, пахне зрадою , нагадування надіслано",

    text_for_dchannel="Літній розпродаж закінчився, а хтось (<@{}>) так і не купив що мав купити (",

    need_format=['text_for_dchannel']

)

counter_message = EventTexts(
    text_for_user=None,

    text_for_admin="Ні, ще не купив ( ",

    text_for_dchannel=None,

    need_format=None
)

EVENTS = {
    "counter_message": counter_message,

    "game_bought": game_bought,
    "sale_ends_soon": sale_ends_soon,
    "sale_ended": sale_ended,
}


def get_event_text(event, *f_args, **f_kwargs):
    event_text = EVENTS[event].format(*f_args, **f_kwargs)

    return event_text.get_texts()
