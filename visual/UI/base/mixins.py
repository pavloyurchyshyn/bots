from visual.UI.base.button import Button


class CreateButtonMixin:
    def create_button_from_data(self, buttons_data: dict):
        buttons = []
        for button_name, button_data in buttons_data.items():
            b = Button(*button_data.get('args', ()),
                       **button_data.get('kwargs', {}),
                       parent=self)
            buttons.append(b)
            setattr(self, button_name, b)

        buttons.sort(key=lambda e: e.y, reverse=True)
        buttons.sort(key=lambda e: e.layer, reverse=True)

        return buttons
