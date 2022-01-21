import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"
terminal = guess_terminal()
myBrowser = "brave"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
	Key([mod], "b",
		lazy.spawn(myBrowser),
		desc='Brave browser'
		),
	Key([mod, "shift"], "f",
        lazy.spawn("thunar"),
        desc = 'File manager'
        ),
	Key([mod], "f",
		lazy.window.toggle_fullscreen(),
		desc='toggle fullscreen'
		),
    Key([mod], "c",
        lazy.spawn("codium"),
        desc = 'VSCodium'
        ),
    Key([mod], "l",
        lazy.spawn("lxlock"),
        desc='Lock session'
        ),

    # Switch between windows
    #Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    #Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    #Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "space", lazy.layout.next(),
        #desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = []

group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft"]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 "]
group_labels = ["sys", "www", "dev", "file", "doc"]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
	groups.append(
		Group(
			name=group_names[i],
			layout=group_layouts[i].lower(),
			label=group_labels[i]
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

layout_theme = {"border_width": 2,
                "margin": 10,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    # layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
	layout.MonadTall(**layout_theme),
    # layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.RatioTile(**layout_theme),
	layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "c678dd",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
]

### WIDGET SETTINGS
colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive 

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widget_defaults = dict(
    font="Ubuntu Mono Nerd Font",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)

extension_defaults = widget_defaults.copy()
def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
            ),
        widget.TextBox(
            text = " ",
            background = colors[0],
            foreground = colors[5],
            padding = 3,
            fontsize = 18,
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
            ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
            ),
        widget.GroupBox(
            #font = "Ubuntu Bold",
			font = "MesloLGS NF",
            fontsize = 12,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors[2],
            inactive = colors[7],
            rounded = False,
            highlight_color = colors[1],
            highlight_method = "line",
            this_current_screen_border = colors[6],
            this_screen_border = colors [4],
            other_current_screen_border = colors[6],
            other_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]
            ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = '474747',
            padding = 2,
            fontsize = 14
            ),
		widget.Prompt(
            prompt = prompt,
            font = "Ubuntu Mono",
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[2],
            background = colors[0],
            padding = 0,
            scale = 0.7
            ),
        widget.CurrentLayout(
            foreground = colors[2],
            background = colors[0],
            padding = 5
            ),
        widget.TextBox(
            text = '|',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = '474747',
            padding = 2,
            fontsize = 14
            ),
        widget.WindowName(
            foreground = colors[6],
            background = colors[0],
            padding = 0
            ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[0],
            background = colors[0]
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[0],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[2],
            padding = 3,
            fontsize = 20
            ),
        widget.Net(
            interface = "wlp9s0",
            format = '{down} ↓↑ {up}',
            foreground = colors[2],
            background = colors[5],
            padding = 5
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            font = 'MesloLGS NF',
            text = "",
            background = colors[4],
            foreground = colors[2],
            padding = 0,
            fontsize = 12
            ),
        widget.ThermalSensor(
            foreground = colors[2],
            background = colors[4],
            threshold = 90,
            fmt = '{}',
            padding = 5
            ),
        widget.TextBox(
            text='',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 33
            ),
		widget.TextBox(
            text = "⟳",
            padding = 3,
            foreground = colors[2],
            background = colors[5],
            fontsize = 20
            ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = "Updates: {updates} ",
            foreground = colors[2],
            colour_have_updates = colors[2],
            colour_no_updates = colors[1],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
            padding = 5,
            background = colors[5]
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[2],
            padding = 3,
            fontsize = 20
            ),
        widget.Memory(
            foreground = colors[2],
            background = colors[4],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
            fmt = '{}',
            padding = 5
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = '墳',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[2],
            padding = 3,
            fontsize = 20
            ),
        widget.Volume(
            foreground = colors[2],
            background = colors[5],
            fmt = '{}',
            padding = 5
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[2],
            padding = 3,
            fontsize = 20
            ),
        widget.OpenWeather(
            foreground = colors[2],
            background = colors[4],
			cityid = 2996568,
            padding = 5,
			format = '{location_city} | {main_temp}°{units_temperature} | {weather_details}'
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
		widget.Battery(
            background = colors[5],
            foreground = colors[2],
			padding = 5,
            notify_below = 30,
			format = '{percent:2.0%} {hour:d}:{min:02d}'
			),
		widget.BatteryIcon(
            background = colors[5]
			),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            background = colors[4],
            foreground = colors[2],
            padding = 3,
            fontsize = 14
            ),
        widget.Clock(
            foreground = colors[2],
            background = colors[4],
            format = "%A %d %B - %H:%M "
            ),
        widget.Systray(
            background = colors[1]
        ),
        widget.TextBox(
            text = '',
            font = "Ubuntu Mono",
            foreground = colors[2],
            background = colors[1],
            padding = 8,
            fontsize = 20,
            mouse_callbacks = {'Button1': lazy.spawn("lxsession-logout")},
            ),
        ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
##wmname = "LG3D"
wmname = "Qtile"
