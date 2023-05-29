from enum import Enum


class Attrs:
    Shape = 'shape_class'
    UID = 'uid'
    XK = 'x_k'
    YK = 'y_k'
    Layer = 'layer'
    Text = 'text'
    TextKwargs = 'text_kwargs'
    ButtonKwargs = 'button_kwargs'

    Style = 'style'

    CollideAble = 'collideable'

    PostponeBuild = 'postpone_build'

    HSizeK = 'h_size_k'
    VSizeK = 'v_size_k'
    RectSize = 'rect_size'
    UnlimitedHSize = 'unlimited_h_size'
    UnlimitedVSize = 'unlimited_v_size'
    Parent = 'parent'
    ParentSurface = 'parent_surface'
    Active = 'active'
    Visible = 'visible'

    AutoDraw = 'auto_draw'
    BuildSurface = 'build_surface'


class StyleAttrs(Enum):
    Color: str = 'color'
    FromLeft: str = 'from_left'
    FromBot: str = 'from_bot'
    FromTop: str = 'from_top'

    TextBackColor: str = 'text_back_color'

    SurfaceTransparent: str = 'surface_transparent'
    SurfaceColor: str = 'surface_color'
    SurfaceFlags: str = 'surface_flags'
    AA: str = 'antialiasing'
    AAText: str = 'antialiasing_text'

    BorderColor: str = 'border_color'
    InacBorderColor: str = 'inacborder_color'
    BorderSize: str = 'border_size'
    BorderRadius: str = 'border_radius'
    BorderTopLeftRadius: str = 'border_top_left_radius'
    BorderTopRightRadius: str = 'border_top_right_radius'
    BorderBottomLeftRadius: str = 'border_bottom_left_radius'
    BorderBottomRightRadius: str = 'border_bottom_right_radius'


class TextAttrs(Attrs):
    Color = 'color'
    FontSize = 'font_size'
    FontName = 'font_name'
    ScaleFont = 'scale_font'
    RawText = 'raw_text'
    SplitLines = 'split_lines'
    SplitWords = 'split_words'
    FromLeft = 'from_left'


class InputAttr(Attrs):
    OnEnterAction = 'on_enter_action'
    OnUnfocusAction = 'on_unfocus_action'
    DefaultText = 'default_text'
    DefaultTextColor = 'default_text_color'


class ButtonAttrs(Attrs):
    InacTextKwargs = 'inactive_text_kwargs'

    OnClickAction = 'on_click_action'
    OnClickActionArgs = 'on_click_action_args'
    OnClickActionKwargs = 'on_click_action_kwargs'

    InactiveAfterClick = 'inactive_after_click'
    InvisAfterClick = 'invisible_after_click'


class ButtonStyleAttrs(Enum):
    InacSurfaceTransparent: str = 'inac_surface_transparent'
    InacSurfaceColor: str = 'inac_surface_color'
    InacSurfaceFlags: str = 'inac_surface_flags'
