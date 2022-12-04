class Attrs:
    Shape = 'shape_class'
    UID = 'uid'
    XK = 'x_k'
    YK = 'y_k'
    Layer = 'layer'
    Text = 'text'
    TextData = 'text_data'
    TextKwargs = 'text_kwargs'

    CollideAble = 'collideable'

    PostponeBuild = 'postpone_build'

    HSizeK = 'h_size_k'
    VSizeK = 'v_size_k'
    RectSize = 'rect_size'
    UnlimitedHSize = 'unlimited_h_size'
    UnlimitedVSize = 'unlimited_v_size'
    Parent = 'parent'
    ParentSurface = 'parent_surface'
    Visible = 'visible'
    Active = 'active'

    TextBackColor = 'text_background_color'
    FromLeft = 'from_left'
    FromBot = 'from_bot'
    FromTop = 'from_top'
    # InCenter = 'keep_in_center'
    # PlaceInside = 'place_inside'
    AA = 'antialiasing'

    AutoDraw = 'auto_draw'

    SurfaceTransparent = 'surface_transparent'
    SurfaceColor = 'surface_color'
    SurfaceFlags = 'surface_flags'

    BorderColor = 'border_color'
    InacBorderColor = 'inacborder_color'
    BorderSize = 'border_size'
    BorderRadius = 'border_radius'
    BorderTopLeftRadius = 'border_top_left_radius'
    BorderTopRightRadius = 'border_top_right_radius'
    BorderBottomLeftRadius = 'border_bottom_left_radius'
    BorderBottomRightRadius = 'border_bottom_right_radius'


class TextAttrs(Attrs):
    Color = 'color'
    FontSize = 'font_size'
    FontName = 'font_name'
    ScaleFont = 'scale_font'
    RawText = 'raw_text'
    SplitLines = 'split_lines'


class InputAttr(Attrs):
    OnEnterAction = 'on_enter_action'
    DefaultText = 'default_text'
    DefaultTextColor = 'default_text_color'


class ButtonAttrs(Attrs):
    InacTextKwargs = 'inactive_text_kwargs'

    InacSurfaceTransparent = 'inac_surface_transparent'
    InacSurfaceColor = 'inac_surface_color'
    InacSurfaceFlags = 'inac_surface_flags'

    OnClickAction = 'on_click_action'
    OnClickActionArgs = 'on_click_action_args'
    OnClickActionKwargs = 'on_click_action_kwargs'

    InactiveAfterClick = 'inactive_after_click'
    InvisAfterClick = 'invisible_after_click'
