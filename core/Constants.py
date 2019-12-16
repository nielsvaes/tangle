from PyQt5.QtGui import *

class IO():
    input = "input"
    output = "output"
    both = "output"

    execution_input = "execution_input"
    execution_output = "execution_output"


class Colors():
    # core colors
    node_normal_border       = QColor(36, 66, 114, 255)
    node_hover_border        = QColor(199, 168, 58, 255)
    node_selected_border     = QColor(255, 216, 74, 255)

    node_normal_background   = QColor(65, 65, 65, 255)
    node_hover_background    = QColor(75, 75, 75, 255)
    node_selected_background = QColor(75, 75, 75, 255)

    group_background         = QColor(50, 0, 0, 127)

    connection_normal        = QColor(150, 150, 150, 255)
    connection_hover         = QColor(199, 168, 58, 255)
    connection_selected      = QColor(255, 216, 74, 255)

    socket_output            = QColor(255, 220, 105, 255)
    socket_input             = QColor(105, 255, 110, 255)

    text_default             = QColor(200, 200, 200, 255)
    gray                     = QColor(80, 80, 80, 255)
    white                    = QColor(255, 255, 255, 255)
    black                    = QColor(0, 0, 0, 255)
    red                      = QColor(221, 119, 119, 255)
    green                    = QColor(119, 221, 119, 255)
    blue                     = QColor(119, 119, 211, 255)

    node_scene_computed      = QColor(43, 43, 43, 255)
    node_scene_dirty         = QColor(53, 43, 43, 255)

    # image node colors
    load_image               = QColor(90, 112, 35)
    save_image               = QColor(90, 112, 35)
    split_channel            = QColor(35, 112, 68)
    combine_channel          = QColor(35, 112, 68)
    color_to_gray            = QColor(24, 77, 89)
    gray_to_color            = QColor(24, 77, 89)
    rgb_to_rgba              = QColor(43, 143, 166)
    rgba_to_rgb              = QColor(43, 143, 166)
    blur                     = QColor(24, 89, 62)
    brightness               = QColor(24, 43, 89)
    combine                  = QColor(81, 24, 89)
    contrast                 = QColor(89, 24, 64)
    equalize                 = QColor(89, 24, 33)
    invert                   = QColor(24, 89, 38)
    mask_color               = QColor(90, 94, 26)
    saturation               = QColor(94, 42, 26)
    sharpen                  = QColor(11, 138, 119)
    enlarge                  = QColor(140, 100, 83)
    shrink                   = QColor(138, 120, 113)
    mirror                   = QColor(42, 82, 80)
    rotate                   = QColor(27, 62, 143)

    # math colors
    float                    = QColor(83, 158, 68)
    add_float                = QColor(25, 92, 100)
    multiply_float           = QColor(50, 92, 125)
    power_float              = QColor(75, 92, 150)
    subtract_float           = QColor(100, 92, 175)
    divide_float             = QColor(150, 92, 200)
    vector2                  = QColor(62, 96, 92)
    vector3                  = QColor(62, 106, 92)

    # text colors
    string                   = QColor(127, 127, 255)
    replace_string           = QColor(127, 127, 127)

    # others
    lists                    = QColor(80, 127, 80)

    # graphing
    plot                     = QColor(255, 0, 255, 255)
    average_graph            = QColor(170, 0, 255, 170)

class NumberConstants():
    connection_width_normal    = 2
    connection_width_hover     = connection_width_normal * 1.5
    connection_width_selected  = connection_width_normal * 1.75

    execution_connection_width = 3

    title_offset = 2
    title_label_size = 18
    title_background_height = 30

    socket_size          = 20
    socket_label_spacing = socket_size * 1.1
    socket_spacing       = 5
    socket_z_depth       = 110

    connection_z_depth_normal = 1
    connection_z_depth_hover  = 50

    group_z_depth = 0

    connection_cv_offset = 30

    node_item_border_width_selected = 4
    node_item_height                = socket_size
    node_item_width                 = node_item_height * 7
    node_item_z_depth               = 100

nc = NumberConstants

class StyleSheets():
    bold_12pt = "font-weight: bold; font: 12pt"
    values_title = "font-weight: bold; font: 12pt; border: 1px; border-radius: 6px;"

    socket_ui_connected = "QDoubleSpinBox{background: rgb(239, 239, 119); } QLineEdit {background-color: rgb(239, 239, 119); }"
    node_result_calculated = "QDoubleSpinBox{background: rgb(73, 143, 255); } QLineEdit {background-color: rgb(73, 143, 255); }"

    view_dirty = "border-color: rgb(149, 72, 17); border: 2px; "

ss = StyleSheets

