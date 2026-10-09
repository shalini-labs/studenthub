
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from database import create_database, add_student, get_students


Window.title = "StudentHub | Student Management System"
Window.size = (1100, 720)
Window.minimum_width = 850
Window.minimum_height = 600


BLUE = (0.12, 0.38, 0.85, 1)
DARK = (0.12, 0.16, 0.24, 1)
BG = (0.95, 0.97, 0.99, 1)
WHITE = (1, 1, 1, 1)
MUTED = (0.45, 0.49, 0.56, 1)


class Panel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*WHITE)
            self.panel_bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.panel_bg.pos = self.pos
        self.panel_bg.size = self.size


class StudentHubApp(App):

    def build(self):
        self.manager = ScreenManager()

        self.manager.add_widget(
            self.create_screen("Dashboard", "dashboard")
        )
        self.manager.add_widget(
            self.create_screen("Students", "students")
        )
        self.manager.add_widget(
            self.create_screen("Academic", "academic")
        )
        self.manager.add_widget(
            self.create_screen("Settings", "settings")
        )

        self.manager.current = "dashboard"
        return self.manager

    def create_screen(self, title, screen_name):
        screen = Screen(name=screen_name)

        root = BoxLayout(
            orientation="horizontal",
            spacing=0
        )

        # Left sidebar
        sidebar = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=215,
            padding=[15, 22, 15, 15],
            spacing=12
        )
        sidebar.canvas.before.clear()

        with sidebar.canvas.before:
            Color(*WHITE)
            sidebar_bg = RoundedRectangle(
                pos=sidebar.pos,
                size=sidebar.size,
                radius=[0]
            )

        def update_sidebar(*args):
            sidebar_bg.pos = sidebar.pos
            sidebar_bg.size = sidebar.size

        sidebar.bind(pos=update_sidebar, size=update_sidebar)

        logo = Label(
            text="[b]StudentHub[/b]",
            markup=True,
            font_size=25,
            color=BLUE,
            size_hint_y=None,
            height=55
        )
        sidebar.add_widget(logo)

        tagline = Label(
            text="STUDENT MANAGEMENT",
            font_size=10,
            color=MUTED,
            size_hint_y=None,
            height=25
        )
        sidebar.add_widget(tagline)

        sidebar.add_widget(
            self.make_nav_button("Dashboard", "dashboard")
        )
        sidebar.add_widget(
            self.make_nav_button("Students", "students")
        )
        sidebar.add_widget(
            self.make_nav_button("Academic", "academic")
        )

        spacer = BoxLayout()
        sidebar.add_widget(spacer)

        sidebar.add_widget(
            self.make_nav_button("Settings", "settings")
        )

        # Main content area
        content = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=18
        )

        with content.canvas.before:
            Color(*BG)
            content_bg = RoundedRectangle(
                pos=content.pos,
                size=content.size,
                radius=[0]
            )

        def update_content_bg(*args):
            content_bg.pos = content.pos
            content_bg.size = content.size

        content.bind(pos=update_content_bg, size=update_content_bg)

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=75,
            spacing=3
        )

        header.add_widget(
            Label(
                text=f"[b]{title}[/b]",
                markup=True,
                font_size=27,
                color=DARK,
                halign="left",
                valign="middle"
            )
        )

        header.add_widget(
            Label(
                text="Welcome back! Here is your overview.",
                font_size=13,
                color=MUTED,
                halign="left"
            )
        )

        content.add_widget(header)

        if screen_name == "dashboard":
            self.add_dashboard_content(content)
        else:
            content.add_widget(
                Panel(
                    orientation="vertical",
                    padding=25,
                    spacing=12,
                    children=[]
                )
            )
            placeholder = content.children[0]
            placeholder.add_widget(
                Label(
                    text=f"[b]{title}[/b]",
                    markup=True,
                    font_size=23,
                    color=DARK
                )
            )
            placeholder.add_widget(
                Label(
                    text="This section will be developed next.",
                    font_size=15,
                    color=MUTED
                )
            )

        root.add_widget(sidebar)
        root.add_widget(content)
        screen.add_widget(root)

        return screen

    def make_nav_button(self, text, screen_name):
        btn = Button(
            text=text,
            size_hint_y=None,
            height=46,
            font_size=15,
            color=BLUE if self.manager.current == screen_name
            else DARK,
            background_normal="",
            background_color=(0.90, 0.94, 1, 1)
            if self.manager.current == screen_name
            else (1, 1, 1, 1)
        )

        btn.bind(
            on_press=lambda instance:
            setattr(self.manager, "current", screen_name)
        )

        return btn

    def add_dashboard_content(self, content):
        # Statistics cards
        stats = GridLayout(
            cols=3,
            spacing=15,
            size_hint_y=None,
            height=125
        )

        cards = [
            ("Total Students", "0", "Registered students"),
            ("Attendance", "0%", "Overall attendance"),
            ("Academic Records", "0", "Records available")
        ]

        for heading, value, description in cards:
            card = Panel(
                orientation="vertical",
                padding=15,
                spacing=5
            )

            card.add_widget(
                Label(
                    text=heading,
                    font_size=14,
                    color=MUTED
                )
            )

            card.add_widget(
                Label(
                    text=f"[b]{value}[/b]",
                    markup=True,
                    font_size=27,
                    color=BLUE
                )
            )

            card.add_widget(
                Label(
                    text=description,
                    font_size=11,
                    color=MUTED
                )
            )

            stats.add_widget(card)

        content.add_widget(stats)

        # Welcome panel
        welcome = Panel(
            orientation="vertical",
            padding=25,
            spacing=12
        )

        welcome.add_widget(
            Label(
                text="[b]Welcome to StudentHub![/b]",
                markup=True,
                font_size=23,
                color=DARK,
                halign="left"
            )
        )

        welcome.add_widget(
            Label(
                text=(
                    "Manage student information, academic results "
                    "and attendance from one place."
                ),
                font_size=14,
                color=MUTED,
                halign="left"
            )
        )

        content.add_widget(welcome)

        # Quick actions
        content.add_widget(
            Label(
                text="[b]Quick Access[/b]",
                markup=True,
                font_size=19,
                color=DARK,
                size_hint_y=None,
                height=35,
                halign="left"
            )
        )

        actions = GridLayout(
            cols=2,
            spacing=15,
            size_hint_y=None,
            height=110
        )

        students_btn = Button(
            text="Manage Students",
            background_normal="",
            background_color=BLUE,
            color=WHITE,
            font_size=16
        )
        students_btn.bind(
            on_press=lambda instance:
            setattr(self.manager, "current", "students")
        )

        academic_btn = Button(
            text="Academic Records",
            background_normal="",
            background_color=(0.16, 0.60, 0.43, 1),
            color=WHITE,
            font_size=16
        )
        academic_btn.bind(
            on_press=lambda instance:
            setattr(self.manager, "current", "academic")
        )

        actions.add_widget(students_btn)
        actions.add_widget(academic_btn)
        content.add_widget(actions)

        content.add_widget(
            Label(
                text="StudentHub  |  Your student data, organized.",
                font_size=12,
                color=MUTED,
                size_hint_y=None,
                height=25
            )
        )


if __name__ == "__main__":
    StudentHubApp().run()