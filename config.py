import os
import subprocess
from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Match

wmname = "LG3D" # solve the java problem
mod = 'mod4'

# Key bindings
keys = [
	# Window manager controls
	Key([mod, 'control'], 'r', lazy.restart()),
	Key([mod, 'control'], 'q', lazy.shutdown()),
	Key([mod], 'r', lazy.spawn('rofi -show drun -show-icons -modi')),
	Key([mod], 'Return', lazy.spawn('lxterminal')),
	Key([mod], 'f', lazy.spawn('firefox')),
	Key([mod], 't', lazy.spawn('thunar')),
	Key([mod], 'l', lazy.spawn(os.path.expanduser('~/.config/qtile/blur-lock.sh'))),
	Key([mod], 'w',      lazy.window.kill()),

	Key([mod], 'Tab', lazy.layout.next()),
	Key([mod], 'Left', lazy.screen.prevgroup()),
	Key([mod], 'Right', lazy.screen.nextgroup()),
	
	# Layout ratio
	Key([mod], 'i', lazy.layout.increase_ratio()),
	Key([mod], 'p', lazy.layout.decrease_ratio()),

	# Layout modification
	Key([mod, 'control'], 'space', lazy.window.toggle_floating()),

	# Switch between windows in current stack pane
	Key([mod], 'Up', lazy.layout.down()),
	Key([mod], 'Down', lazy.layout.up()),

	# Move windows up or down in current stack
	Key([mod, 'control'], 'Left', lazy.layout.shuffle_down()),
	Key([mod, 'control'], 'Right', lazy.layout.shuffle_up()),

	# Switch window focus to other pane(s) of stack
	Key([mod], 'space', lazy.layout.next()),

	# Toggle between different layouts as defined below
	Key([mod], 'Tab',    lazy.next_layout()),
	
	# Power
	Key([mod, 'shift'], 'r', lazy.spawn('reboot')),
	Key([mod, 'shift'], 'p', lazy.spawn('poweroff')),
	
	# Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 10"))
]

# Mouse bindings and options
mouse = (
	Drag([mod], 'Button1', lazy.window.set_position_floating(),
		start=lazy.window.get_position()),
	Drag([mod], 'Button3', lazy.window.set_size_floating(),
		start=lazy.window.get_size()),
)

bring_front_click = True
cursor_warp = False
follow_mouse_focus = True

# Groups
groups = [
    Group('  Home', matches=[Match(wm_class=["Thunar"])] ),
    Group('  Media', matches=[Match(wm_class=["vlc"])] ),
    Group('  Dev', matches=[Match(wm_class=["Geany", "zeal", "jetbrains-pycharm-ce", "java-lang-Thread"])] ),
    Group('  Terminal', matches=[Match(wm_class=["Lxterminal"])] ),
    Group('  Web', matches=[Match(wm_class=["Firefox","TelegramDesktop"])] ),
    Group('  ESP32', matches=[Match(wm_class=["processing-app-Base", "Code"])]),
    Group('  Other', matches=[Match(wm_class=["libreoffice", "soffice"])]),
    
]

grplist = []
# Make group list with respective integers
for i in range(len(groups)):
    grplist.append(i)

# Start the integer from one to bind it later
grplist.remove(0)
grplist.append(len(grplist)+1)

# Iterate and bind index as key
for k, v in zip(grplist, groups):
    keys.extend([
        # mod1 + letter of group = switch to grouplazy.group[j].toscreen()
        Key([mod], str(k), lazy.group[v.name].toscreen()),

        # mod1 + shift + letter of group = switch to
        # & move focused window to group
        Key([mod, "shift"], str(k), lazy.window.togroup(v.name)),
    ])



dgroups_key_binder = None
dgroups_app_rules = []

# Layouts
layouts = [
	layout.Max(),
	layout.Stack(num_stacks=2),
	layout.Tile(),
	layout.RatioTile(),
	layout.Matrix(),
]



# Screens and widget options
screens = [
	Screen(
		top=bar.Bar(
			widgets=[
				widget.GroupBox(
					highlight_method='block',
					inactive='999999'
				),
				widget.CurrentLayout(
					padding=5
				),
				widget.WindowName(),
				widget.KeyboardLayout(
					configured_keyboards=['us','ar'],
					option='grp:alt_shift_toggle'
				),
				widget.Systray(),
				widget.Battery(),
				widget.Clock(format='%a %d %b %I:%M %p'),
			],
			size=25,
			background=['222222', '111111'],
			
		),
	),
]

widget_defaults = dict(
	font='MADE Evolve Sans EVO',
	fontsize=13,
)

floating_layout = layout.Floating(
    border_normal='000000',
    border_focus='999999',
    border_width=3,
    auto_float_types=[
        'utility',
        'notification',
        'toolbar',
        'splash',
        'dialog',
    ],
    float_rules=[
        {'wmclass': 'confirm'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'gcr-prompter'},
        {'wmclass': 'confirmreset'},
        {'wmclass': 'makebranch'},
        {'wmclass': 'maketag'},
        {'wmclass': 'peek'},
        {'wname': 'branchdialog'},
        {'wname': 'pinentry'},
        {'wmclass': 'ssh-askpass'},
        {'wmclass': 'lxpolkit'},
        {'wmclass': 'java-lang-Thread'},
    ]
)
auto_fullscreen = True

#@hook.subscribe.client_new
#def java(window):
#    try:
#        if 'sun-awt-X11-XFramePeer' in window.window.get_wm_class():
#            window.java = True
#        else:
#            window.java = False
#    except:
#    window.java = False

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


@hook.subscribe.startup_once
def autostart():
	home = os.path.expanduser('~/.config/qtile/autostart.sh')
	subprocess.call([home])
   

@hook.subscribe.layout_change
def update_layout_name(lay, group):
    """
        @type lay: Layout
        @type group: _Group
    """
    layout_name_widget.update(lay.name)


@hook.subscribe.client_new
def java(win):
    try:
        if 'sun-awt-X11-XFramePeer' in win.window.get_wm_class():
            win.java = True
        else:
            win.java = False
    except:
        win.java = False
    
