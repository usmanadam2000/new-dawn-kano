import datetime
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivymd.uix.dropdownitem import MDDropDownItem

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivy.uix.scrollview import ScrollView
import sqlite3
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
import bcrypt
from kivy.uix.image import Image, AsyncImage
from kivy.core.window import Window
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList, IconLeftWidget

Window.size = (300, 500)

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '12dp'
        padding: '24dp'
        MDLabel:
            text: 'New Dawn Inventory'
            halign: 'center'
            font_style: 'H4'
            font_size: sp(15)
            color: [1,1,1,1]
            bold: True

        MDTextField:
            id: username_input
            hint_text: 'Username'
            multiline: False
            size_hint_y: None
            height: '48dp'
            icon_right: 'account'

        MDTextField:
            id: password_input
            hint_text: 'Password'
            multiline: False
            password: True
            size_hint_y: None
            height: '48dp'
            icon_right: 'eye-off'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: '40dp'
            spacing: '12dp'
            pos_hint: {'center_x': 0.5}

            MDRaisedButton:
                text: 'Login'
                size_hint_x: None
                width: '120dp'
                on_release: root.login()

            MDRaisedButton:
                text: 'Register'
                size_hint_x: None
                width: '120dp'
                on_release: root.goto_register()
<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '12dp'
        padding: '24dp'
        MDLabel:
            text: 'Register'
            halign: 'center'
            font_style: 'H4'
            font_size: sp(12)
            color: [1,1,1,1]
            bold: True

        Spinner:  # Use Spinner instead of MDSpinner
            id: role_spinner
            text: 'Select Role'
            values: ['User', 'Viewer']
            size_hint_y: None
            height: '48dp'

        MDTextField:
            id: username_input
            hint_text: 'Username'
            multiline: False
            size_hint_y: None
            height: '48dp'
            icon_right: 'account'


        MDTextField:
            id: password_input
            hint_text: 'Password'
            multiline: False
            password: True
            size_hint_y: None
            height: '48dp'
            icon_right: 'eye-off'

        MDTextField:
            id: phone_input
            hint_text: 'Phone Number'
            multiline: False
            input_type: 'number'
            size_hint_y: None
            height: '48dp'
            icon_right: 'phone'

        MDTextField:
            id: email_input
            hint_text: 'Email Address'
            multiline: False
            input_type: 'text'
            size_hint_y: None
            height: '48dp'
            icon_right: 'email'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: '40dp'
            spacing: '12dp'
            pos_hint: {'center_x': 0.5}

            MDRaisedButton:
                text: 'Register'
                size_hint_x: None
                width: '120dp'
                on_release: root.register()

            MDRaisedButton:
                text: 'Back'
                size_hint_x: None
                width: '120dp'
                on_release: root.goto_login()

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_normal
        spacing: '12dp'
        padding: '24dp'

        MDTopAppBar:
            title: 'Fantel Nig.'  # Set the title of the top app bar
            left_action_items: [['menu', lambda x: root.open_menu()]]  # Add menu icon

        MDLabel:
            text: 'Welcome to New Dawn Inventory'
            halign: 'center'
            font_style: 'H4'
            font_size: sp(16)
            color: [1,1,1,1]
            bold: True

<AddStockScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '6dp'
        padding: '12dp'

        Spinner:
            id: stock_spinner
            text: "Select an item"
            values: root.get_inventory_items()
            on_text: root.on_item_selected(self.text)
            size_hint: (1, None)
            height: '48dp'

        MDTextField:
            id: stock_name_input
            hint_text: 'Stock Name'
            multiline: False
            size_hint: (1, None)
            height: '48dp'
            width: "260dp"
            icon_right: 'text-box-multiple'

        MDTextField:
            id: quantity_input
            hint_text: 'Quantity'
            input_type: 'number'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'calculator'

        MDTextField:
            id: old_purchase_price_input
            hint_text: 'Old Purchase Price'
            input_type: 'number'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'currency-usd'

        MDTextField:
            id: old_selling_price_input
            hint_text: 'Old Selling Price'
            input_type: 'number'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'currency-usd'

        MDTextField:
            id: new_purchase_price_input
            hint_text: 'New Purchase Price'
            input_type: 'number'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'currency-usd'

        MDTextField:
            id: new_selling_price_input
            hint_text: 'New Selling Price'
            input_type: 'number'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'currency-usd'

        MDRaisedButton:
            text: 'Date'
            on_release: root.open_date_picker()

        MDTextField:
            id: date_input
            hint_text: 'Date'
            readonly: True
            multiline: False
            size_hint: (1, None)
            height: "48dp"
            width: "260dp"
            icon_right: 'calendar'

        MDTextField:
            id: serial_no_input
            hint_text: 'Serial No.'
            multiline: False
            size_hint: (1, None)
            width: "260dp"
            height: "48dp"
            icon_right: 'barcode-scan'

        BoxLayout:
            spacing: '12dp'
            size_hint: (1, None)
            height: '48dp'

            MDRaisedButton:
                text: 'Add Stock'
                on_release: root.add_stock()

            MDRaisedButton:
                text: 'Back Home'
                on_release: root.back_to_home()

<ReturnedStockScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        MDRaisedButton:
            text: 'Refresh'
            size_hint_x: None
            width: '200dp'
            on_release: root.refresh_stock_list()
            pos_hint: {'center_x': .5}
            
        Spinner:
            id: stock_spinner
            text: "Select Stock"
            values: []  # Values will be populated in Python
            size_hint_y: None
            height: '38dp'

        MDTextField:
            id: ccr_name_input
            hint_text: 'CCR Name'
            multiline: False
            size_hint_y: None
            height: '30dp'
            icon_right: 'account'

        MDTextField:
            id: quantity_input
            hint_text: 'Quantity Returned'
            multiline: False
            input_type: 'number'
            size_hint_y: None
            height: '30dp'
            icon_right: 'plus-minus'

        BoxLayout:
            orientation: 'vertical'
            spacing: '10dp'
            padding: '10dp'

            MDRaisedButton:
                text: 'Date'
                pos_hint: {'center_x': .5}
                on_release: root.open_date_picker()


            MDTextField:
                id: date_input
                hint_text: 'Date'
                multiline: False
                size_hint_y: None
                height: '30dp'
                icon_right: 'calendar'

            MDRaisedButton:
                text: 'Time'
                pos_hint: {'center_x': .5}
                on_release: root.open_time_picker()

            MDTextField:
                id: time_input
                hint_text: 'Time'
                multiline: False
                size_hint_y: None
                height: '30dp'
                icon_right: 'clock'

        BoxLayout:
            orientation: 'horizontal'
            spacing: '10dp'
            padding: '10dp'

            MDRaisedButton:
                text: 'Update Quantity'
                size_hint_x: None
                width: '200dp'
                on_release: root.update_quantity()
                pos_hint: {'center_x': .5}


            MDRaisedButton:
                text: 'Back'
                size_hint_x: None
                width: '200dp'
                on_release: root.back_to_home()
                pos_hint: {'center_x': .5}

""")


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if not username or not password:
            self.show_input_error_dialog()
            return

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if not user:
            self.show_invalid_credentials_dialog()
            return

        hashed_password = user[2]

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            role = user[0]
            if role == "User":
                self.manager.current = 'home'
            else:  # Viewer
                self.manager.current = 'view_inventory_data'
        else:
            self.show_invalid_credentials_dialog()

    def show_login_success_dialog(self):
        dialog = MDDialog(
            title="Login Successful",
            text="You have successfully logged in.",
            buttons=[
                MDRaisedButton(
                    text="OK", on_release=lambda instance: dialog.dismiss()
                )
            ],
        )
        dialog.open()
        self.manager.current = 'home'

    def show_invalid_credentials_dialog(self):
        dialog = MDDialog(
            title="Invalid Credentials",
            text="The username or password is incorrect.",
            buttons=[
                MDRaisedButton(
                    text="OK", on_release=lambda instance: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def show_input_error_dialog(self):
        dialog = MDDialog(
            title="Input Error",
            text="Please provide both a username and password.",
            buttons=[
                MDRaisedButton(
                    text="OK", on_release=lambda instance: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def goto_register(self):
        self.manager.current = 'register'


class RegisterScreen(Screen):
    def register(self):
        role = self.ids.role_spinner.text
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        phone = self.ids.phone_input.text
        email = self.ids.email_input.text

        if not role or not username or not password or not phone or not email:
            self.show_input_error_dialog()
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = c.fetchone()

        if existing_user:
            self.show_existing_user_error_dialog()
            conn.close()
            return

        c.execute("INSERT INTO users (role, username, password, phone, email) VALUES (?, ?, ?, ?, ?)",
                  (role, username, hashed_password, phone, email))
        conn.commit()
        conn.close()

        if role == "User":
            self.manager.current = 'login'
        else:  # Viewer
            self.manager.current = 'login'

    def show_existing_user_error_dialog(self):
        dialog = MDDialog(
            title="User Exists",
            text="A user with the same username or email already exists.",
            buttons=[
                MDRaisedButton(
                    text="OK", on_release=lambda instance: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def show_input_error_dialog(self):
        dialog = MDDialog(
            title="Input Error",
            text="Please fill in all the required fields.",
            buttons=[
                MDRaisedButton(
                    text="OK", on_release=lambda instance: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def goto_login(self):
        self.manager.current = 'login'


class HomeScreen(Screen):
    def open_menu(self):
        self.drawer.set_state("open")  # Open the drawer when the menu icon is clicked

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)  # Change 'Solar' to 'HomeScreen'
        self.drawer = None

    def on_pre_enter(self):
        self.create_drawer()

    def create_drawer(self):
        if not self.drawer:
            self.drawer = MDNavigationDrawer()

            # Create a drawer content layout
            content_layout = MDBoxLayout(orientation='vertical')

            # Add an image to cover the remaining space
            image = Image(source='fantel_logo.jpg', allow_stretch=True, keep_ratio=False)
            content_layout.add_widget(image)

            # Create and add menu items
            drawer_content = MDList()
            menu_items = [
                ("New Stock", "plus"),
                ("Stock(issuance)", "account-arrow-right"),
                ("Stock(issued)", "history"),
                ("Stock(returning)", "square-edit-outline"),
                ("Stock(returned)", "chart-timeline-variant"),
                ("Selling Price", "currency-ngn"),
                ("View Inventory", "table-eye"),
                ("Stock History Table", "table-large"),
                ("Delete Stock", "delete"),
                ("Logout", "logout"),
            ]

            for text, icon in menu_items:
                menu_item = OneLineIconListItem(text=text)
                menu_item.add_widget(IconLeftWidget(icon=icon))
                drawer_content.add_widget(menu_item)

            # Add the drawer content
            content_layout.add_widget(drawer_content)

            self.drawer.add_widget(content_layout)

            self.add_widget(self.drawer)

            # Set the on_item_click events for the menu items
            for item in drawer_content.children:
                if item.text == "New Stock":
                    item.bind(on_release=self.goto_add_stock_screen)
                elif item.text == "Stock(returning)":
                    item.bind(on_release=self.goto_returned_stock_screen)
                elif item.text == "Delete Stock":
                    item.bind(on_release=self.goto_delete_stock_screen)
                elif item.text == "Stock(issuance)":
                    item.bind(on_release=self.goto_stock_issued_screen)
                elif item.text == "Stock(issued)":
                    item.bind(on_release=self.goto_stock_issued_history_screen)
                elif item.text == "Stock(returned)":
                    item.bind(on_release=self.goto_stock_history_screen)
                elif item.text == "View Inventory":
                    item.bind(on_release=self.goto_view_inventory_screen)
                elif item.text == "Stock History Table":
                    item.bind(on_release=self.goto_stock_history_table_screen)
                elif item.text == "Selling Price":
                    item.bind(on_release=self.goto_selling_price_screen)
                elif item.text == "Logout":
                    item.bind(on_release=self.logout)

    def logout(self, instance):
        self.manager.current = 'login'

    def goto_add_stock_screen(self, instance):
        self.manager.current = 'add_stock'

    def goto_returned_stock_screen(self, instance):
        self.manager.current = 'returned_stock'

    def goto_view_inventory_screen(self, instance):
        self.manager.current = 'view_inventory_data'

    def goto_stock_history_table_screen(self, instance):
        self.manager.current = 'stock_history_table'

    def goto_stock_history_screen(self, instance):
        self.manager.current = 'stock_returned_history'

    def goto_stock_issued_history_screen(self, instance):
        self.manager.current = 'stock_issued_history'

    def goto_stock_issued_screen(self, instance):
        self.manager.current = 'stock_issued'

    def goto_delete_stock_screen(self, instance):
        self.manager.current = 'delete_stock'

    def goto_selling_price_screen(self, instance):
        self.manager.current = 'selling_price'


class AddStockScreen(Screen):
    def __init__(self, **kwargs):
        super(AddStockScreen, self).__init__(**kwargs)
        self.date_input = None  # Initialize date_input
        self.spinner = MDSpinner(active=False)
        self.stock_name_input = self.ids.stock_name_input
        self.stock_spinner = self.ids.stock_spinner
        self.old_purchase_price_input = self.ids.old_purchase_price_input
        self.old_selling_price_input = self.ids.old_selling_price_input
        self.new_purchase_price_input = self.ids.new_purchase_price_input
        self.new_selling_price_input = self.ids.new_selling_price_input
        self.date_dialog = MDDatePicker()
        self.serial_no_input = self.ids.serial_no_input
        # Assign date_input
        self.date_input = self.ids.date_input

        # Initialize the spinner values
        self.stock_spinner.values = self.get_inventory_items()

        self.date_dialog.bind(on_save=self.on_date_selected)

    def get_inventory_items(self):
        # Fetch stock items from the existing method
        stock_items = [
            "Oraimo Charger",
            "Type C to C Charger",
            "Type C to USB Charger",
            "Type C Explore",
            "Iphone X charger",
            "Iphone USB",
            "Shplus Charger",
            "Infinix CA charger",
            "Solar Fan New",
            "MIFI",
            "Smart 7 plus 64-4+3GB",
            "Solar Orbit fan",
            "Solar Adapter AC",
            "Hynet CAT4",
            "itel 5606",
            "Redmi A2+ 32+2",
            "A02",
            "MTN Hynetflex",
            "OALE 2160",
            "MTN PPSK",
            "Redmi A2+ 64+3",
            "solar bulb",
            "MTN Router Deskphone",
            "MTN Smartphone A23",
            "MTN Smartphone A23",
            "A07",
            "Solar bulb",
            "Solar Bulb LED",
            "Solar Inverter",
            "Itel 2163",
            "Lumos Fan",
            "Solar TV Cable",
            "Solar Bulb LED",
            "solar ware",
            "Tecno T101",
            "Redmi 12C 32+3",
            "Tecno T352",
            "ITEL 5636",
            "Vital Phone",
            "TECNO T101",
            "Z Laptop Charger",
            "Z Lufen Deskphone",
            "Z Oale Apex 3",
            "DC Solar Fan",
            "TECNO T101",
            "M1",
            "Redmi 12C 128+4",
            "Extra bass Air peace",
            "Smart 7plus 64+2+2",
            "Sam 1 Airpeace",
            "HOT 20i 64-4GB",
            "Y38 Air peace",
            "H-mobile 5260",
            "PPWB",
            "D-Light",
            "Logical",
            "VTU",
            "MOMO",
            "Others"]

        # Fetch stock items from the new_stock table
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                        CREATE TABLE IF NOT EXISTS new_stock (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock TEXT
                        )
                    ''')
        c.execute("SELECT stock FROM new_stock")
        new_stock_items = [row[0] for row in c.fetchall()]
        conn.close()

        # Combine stock items from both sources
        all_stock_items = stock_items + new_stock_items

        return all_stock_items if all_stock_items else ["Select an item"]  # Default value if the list is empty

    def on_item_selected(self, item):
        print(f"Selected item: {item}")
        if item == "Others":
            self.show_stock_name_input()
        else:
            self.hide_stock_name_input()

    def hide_stock_name_input(self):
        self.ids.stock_name_input.opacity = 0
        self.ids.stock_name_input.text = ""
        self.ids.stock_name_input.disabled = True

    def show_stock_name_input(self):
        self.ids.stock_name_input.opacity = 1
        self.ids.stock_name_input.text = ""
        self.ids.stock_name_input.disabled = False

    def open_date_picker(self):
        self.date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.ids.date_input.text = str(value)

    def add_stock(self):
        selected_stock = self.stock_spinner.text
        quantity = self.ids.quantity_input.text
        old_purchase_price = self.old_purchase_price_input.text
        old_selling_price = self.old_selling_price_input.text
        new_purchase_price = self.new_purchase_price_input.text
        new_selling_price = self.new_selling_price_input.text
        selected_date = self.date_input.text
        serial_no = self.serial_no_input.text

        # Validate input fields
        if not selected_stock or selected_stock.lower() == "select an item":
            self.show_snackbar("Please select a stock name.")
            return

        if not quantity or not new_purchase_price or not new_selling_price:
            self.show_snackbar("Please fill in all fields.")
            return

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        if selected_stock.lower() == "others":
            # Insert data into the stock_inventory table
            c.execute('''
                INSERT INTO stock_inventory (
                    stock, quantity, new_purchase_price, new_selling_price
                ) VALUES (?, ?, ?, ?)
            ''', (self.ids.stock_name_input.text, quantity, new_purchase_price, new_selling_price))

            # Insert data into the stock_history_table
            c.execute('''
                INSERT INTO stock_history_table (
                    stock, quantity, old_purchase_price, old_selling_price,
                    new_purchase_price, new_selling_price, date_added, serial_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.ids.stock_name_input.text, quantity, old_purchase_price, old_selling_price,
                new_purchase_price, new_selling_price, selected_date, serial_no
            ))

            # Insert data into the new_stock table
            c.execute('''
                INSERT INTO new_stock (stock) VALUES (?)
            ''', (self.ids.stock_name_input.text,))
        else:
            # Check if the stock already exists in stock_inventory
            c.execute('SELECT quantity FROM stock_inventory WHERE stock = ?', (selected_stock,))
            existing_quantity = c.fetchone()

            if existing_quantity:
                # Stock exists, update the quantity
                existing_quantity = int(existing_quantity[0])  # Convert to int
                new_quantity = existing_quantity + int(quantity)  # Convert quantity to int before addition
                c.execute('''
                    UPDATE stock_inventory
                    SET quantity = ?, new_purchase_price = ?, new_selling_price = ?
                    WHERE stock = ?
                ''', (new_quantity, new_purchase_price, new_selling_price, selected_stock))
            else:
                # Stock doesn't exist, insert new record
                c.execute('''
                    INSERT INTO stock_inventory (
                        stock, quantity, new_purchase_price, new_selling_price
                    ) VALUES (?, ?, ?, ?)
                ''', (selected_stock, quantity, new_purchase_price, new_selling_price))

            # Insert data into the stock_history_table
            c.execute('''
                INSERT INTO stock_history_table (
                    stock, quantity, old_purchase_price, old_selling_price,
                    new_purchase_price, new_selling_price, date_added, serial_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                selected_stock, quantity, old_purchase_price, old_selling_price,
                new_purchase_price, new_selling_price, selected_date, serial_no
            ))

        conn.commit()
        conn.close()

        self.show_snackbar("Stock added successfully.")

        # Clear input fields
        self.ids.quantity_input.text = ""
        self.old_purchase_price_input.text = ""
        self.old_selling_price_input.text = ""
        self.new_purchase_price_input.text = ""
        self.new_selling_price_input.text = ""
        self.date_input.text = ""
        self.serial_no_input.text = ""
        self.stock_spinner.text = "Select an item"

    def show_snackbar(self, text):
        snackbar = Snackbar(text=text, pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=None, width=dp(300))
        snackbar.open()

    def back_to_home(self):
        self.manager.current = 'home'


class ReturnedStockScreen(Screen):
    def __init__(self, **kwargs):
        super(ReturnedStockScreen, self).__init__(**kwargs)
        self.populate_stock_spinner()
        self.date_dialog = MDDatePicker()
        self.time_dialog = MDTimePicker()

        self.date_dialog.bind(on_save=self.on_date_selected)
        self.time_dialog.bind(on_save=self.on_time_selected)

    def refresh_stock_list(self):
        self.populate_stock_spinner()

    def on_enter(self):
        # Bind the Spinner's text property to the selected_stock property
        app = MDApp.get_running_app()
        self.ids.stock_spinner.text = app.selected_stock

    def populate_stock_spinner(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                        CREATE TABLE IF NOT EXISTS stock_inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock TEXT,
                            quantity INTEGER,
                            new_purchase_price INTEGER,
                            new_selling_price INTEGER
                        )
                    ''')

        # Fetch stock items from the stock_inventory table
        c.execute("SELECT stock FROM stock_inventory")
        stock_items = [row[0] for row in c.fetchall()]
        conn.close()

        # Set the items in the Spinner
        self.ids.stock_spinner.values = stock_items

    def update_quantity(self):
        selected_stock = self.ids.stock_spinner.text
        new_quantity_text = self.ids.quantity_input.text
        ccr_name = self.ids.ccr_name_input.text
        date = self.ids.date_input.text  # Get the selected date
        time = self.ids.time_input.text  # Get the selected time

        if not selected_stock or not ccr_name or not new_quantity_text or not date or not time:
            self.show_snackbar("Please fill in all fields.")
            return

        try:
            new_quantity = int(new_quantity_text)
        except ValueError:
            self.show_snackbar("Quantity must be a valid number.")
            return

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        # Check if the selected stock and CCR combination exists in the stock_issued table
        c.execute('''
            SELECT quantity
            FROM stock_issued
            WHERE stock = ? AND ccr_name = ?
        ''', (selected_stock, ccr_name))
        issued_quantity = c.fetchone()

        if issued_quantity:
            issued_quantity = issued_quantity[0]

            # Check if the returned quantity is less than or equal to the issued quantity
            if new_quantity <= issued_quantity:
                # Calculate the new total quantity in the stock_inventory table
                c.execute('''
                    SELECT quantity
                    FROM stock_inventory
                    WHERE stock = ?
                ''', (selected_stock,))
                current_quantity = c.fetchone()

                if current_quantity:
                    current_quantity = current_quantity[0]
                else:
                    # Handle the case where the selected stock doesn't exist
                    self.show_snackbar("Selected stock doesn't exist in the inventory.")
                    conn.close()
                    return

                new_total_quantity = current_quantity + new_quantity

                # Update the quantity based on the selected stock item in the stock_inventory table
                c.execute('''
                    UPDATE stock_inventory
                    SET quantity = ?
                    WHERE stock = ?
                ''', (new_total_quantity, selected_stock))
                conn.commit()

                # Store the data in the stock_returned_history table
                c.execute('''
                    INSERT INTO stock_returned_history (stock, ccr_name, quantity, date, time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (selected_stock, ccr_name, new_quantity, date, time))
                conn.commit()

                self.show_snackbar("Quantity updated and data stored successfully")
                self.ids.stock_spinner.text = "Select Stock"
                self.ids.ccr_name_input.text = ""
                self.ids.quantity_input.text = ""
                self.ids.date_input.text = ""
                self.ids.time_input.text = ""
            else:
                self.show_snackbar("Returned quantity exceeds the issued quantity.")
        else:
            self.show_snackbar(f"No record found for stock '{selected_stock}' issued to '{ccr_name}'.")

        conn.close()

        self.show_snackbar("Quantity updated and data stored successfully")
        self.ids.stock_spinner.text = "Select Stock"
        self.ids.ccr_name_input.text = ""
        self.ids.quantity_input.text = ""
        self.ids.date_input.text = ""
        self.ids.time_input.text = ""

    def open_date_picker(self):
        self.date_dialog.open()

    def open_time_picker(self):
        self.time_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.ids.date_input.text = str(value)

    def on_time_selected(self, instance, value):
        self.ids.time_input.text = str(value)

    def show_snackbar(self, text):
        snackbar = Snackbar(text=text, pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=None, width=dp(300))
        snackbar.open()

    def back_to_home(self):
        self.manager.current = 'home'


class ViewInventoryScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewInventoryScreen, self).__init__(**kwargs)
        self.data_table = None  # Initialize the MDDataTable
        self.load_inventory_data()

    def load_inventory_data(self, *args):
        # Fetch inventory data from the stock_inventory table
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                        CREATE TABLE IF NOT EXISTS stock_inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock TEXT,
                            quantity INTEGER,
                            new_purchase_price INTEGER,
                            new_selling_price INTEGER
                        )
                    ''')
        c.execute('''
            SELECT stock, quantity, new_purchase_price, new_selling_price
            FROM stock_inventory
            ORDER BY id DESC
        ''')
        inventory_data = c.fetchall()
        conn.close()

        # Create a FloatLayout to manage widget positioning
        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)

        # Create a new MDDataTable
        column_data = [
            ("Stock", dp(40)),
            ("Quantity", dp(20)),
            ("Purchase Price", dp(30)),
            ("Selling Price", dp(20)),
            ("PP Amount", dp(25)),
            ("SP Amount", dp(25))
        ]
        data_table = MDDataTable(check=True, column_data=column_data, rows_num=len(inventory_data) + 1)

        # Add data to the new table
        total_pp_amount = 0
        total_sp_amount = 0
        for stock, quantity, new_purchase_price, new_selling_price in inventory_data:
            pp_amount = new_purchase_price * quantity
            sp_amount = new_selling_price * quantity
            data_table.add_row(
                [stock, str(quantity), str(new_purchase_price), str(new_selling_price), str(pp_amount), str(sp_amount)])
            total_pp_amount += pp_amount
            total_sp_amount += sp_amount

        # Add the "Total" row at the end
        data_table.add_row(['Total', '', '', '', str(total_pp_amount), str(total_sp_amount)])

        # Add the new data table to the layout
        layout.add_widget(data_table)

        refresh_button = MDRaisedButton(
            text='Refresh',
            pos_hint={'center_x': .5},
            on_release=self.load_inventory_data
        )
        layout.add_widget(refresh_button)

        back_button = MDRaisedButton(
            text='Logout',
            pos_hint={'center_x': .5},
            on_release=self.logout
        )
        layout.add_widget(back_button)

        # Clear the old data table (if it exists)
        if self.data_table is not None:
            layout.remove_widget(self.data_table)
            self.data_table = None

        # Add the new layout to the screen
        self.add_widget(layout)

    def logout(self, instance):
        # Navigate back to the home screen
        self.manager.current = 'login'


class DeleteStockScreen(Screen):
    def __init__(self, **kwargs):
        super(DeleteStockScreen, self).__init__(**kwargs)
        self.stock_spinner = Spinner(
            values=[],
            size_hint=(None, None),
            size=(250, 48)
        )
        self.refresh_button = MDRaisedButton(
            text="Refresh",
            size_hint=(None, None),
            size=(100, 48),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        self.refresh_button.bind(on_release=self.refresh_stock_list)

        self.load_stock_items()

        # Add the refresh button to the layout
        self.add_widget(self.refresh_button)

    def load_stock_items(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                        CREATE TABLE IF NOT EXISTS stock_inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock TEXT,
                            quantity INTEGER,
                            new_purchase_price INTEGER,
                            new_selling_price INTEGER
                        )
                    ''')
        # Fetch stock items from the stock_inventory table
        c.execute("SELECT stock FROM stock_inventory")
        stock_items = [row[0] for row in c.fetchall()]

        conn.close()

        if not stock_items:
            # Handle the case where there are no stock items
            self.add_widget(MDLabel(text="No stock items available."))
            return

        # Add an image
        image = AsyncImage(
            source='delete_stock.png',  # Replace 'your_image.png' with the actual image file path
            size_hint=(1, None),
            height='300dp',  # Set the desired height of the image
        )

        self.stock_spinner = Spinner(
            text=stock_items[0],  # Default to the first item
            values=stock_items,
            pos_hint={'center_x': .5},
            size_hint=(None, None),
            size=(250, 48),
        )
        delete_button = MDRaisedButton(
            text='Delete',
            pos_hint={'center_x': .5},
            size_hint=(None, None),
            size=(150, 48),
        )
        delete_button.bind(on_release=self.delete_stock)

        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)
        layout.add_widget(image)
        layout.add_widget(self.stock_spinner)  # Use self.stock_spinner
        layout.add_widget(delete_button)

        back_button = MDRaisedButton(
            text='Back To Home',
            size_hint_x=None,
            width=200,
            pos_hint={'center_x': .5},
            on_release=self.back_to_home,
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

    def delete_stock(self, instance):
        selected_stock = self.stock_spinner.text  # Access stock_spinner directly

        if not selected_stock:
            self.show_snackbar("Please select a stock to delete.")
            return

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                        CREATE TABLE IF NOT EXISTS stock_inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock TEXT,
                            quantity INTEGER,
                            new_purchase_price INTEGER,
                            new_selling_price INTEGER
                        )
                    ''')
        # Check if the selected stock exists in the inventory
        c.execute('''
            SELECT stock
            FROM stock_inventory
            WHERE stock = ?
        ''', (selected_stock,))
        existing_stock = c.fetchone()

        if not existing_stock:
            # Handle the case where the selected stock doesn't exist
            self.show_snackbar("Selected stock doesn't exist in the inventory.")
            conn.close()
            return

        # Delete the selected stock from the stock_inventory table
        c.execute('''
            DELETE FROM stock_inventory
            WHERE stock = ?
        ''', (selected_stock,))
        conn.commit()

        # Remove the deleted stock from the Spinner's values
        self.stock_spinner.values.remove(selected_stock)

        conn.close()

        self.show_snackbar("Stock deleted successfully")
        self.stock_spinner.text = "Select Stock"  # Set the Spinner text after deletion

    def show_snackbar(self, text):
        snackbar = Snackbar(text=text, pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=None, width=dp(300))
        snackbar.open()

    def refresh_stock_list(self, instance):
        # Refresh the stock list in the Spinner
        self.load_stock_items()

    def back_to_home(self, instance):
        self.manager.current = 'home'


class StockIssuedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
        self.conn = sqlite3.connect('user_data.db')
        self.cursor = self.conn.cursor()
        self.create_stock_issued_table()
        self.populate_stock_name_spinner()  # Populate the product name spinner

        # Add a refresh button
        self.refresh_button = MDRaisedButton(
            text="Refresh",
            pos_hint={'center_x': .5, 'center_y': 0.95},
            on_release=self.refresh_stock_list
        )

        self.add_widget(self.refresh_button)

    def create_stock_issued_table(self):
        # Create the 'stockissued' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_issued (
                id INTEGER PRIMARY KEY,
                ccr_name TEXT,
                stock TEXT,
                quantity INTEGER,
                date TEXT,
                time TEXT
            )
        ''')
        self.conn.commit()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=12, spacing=20)

        # Create a text field for CCR Name
        self.ccr_name_input = MDTextField(
            hint_text="CCR Name",
            helper_text="Enter CCR Name",
            helper_text_mode="on_focus",
        )
        layout.add_widget(self.ccr_name_input)

        # Create a spinner for Stock Name
        self.stock_name_spinner = Spinner(
            text="Select Stock Name",  # Initially empty
            values=[],  # Initially empty
            size_hint=(None, None),
            size=(300, 44),
            pos_hint={'center_x': 0.5},
        )
        layout.add_widget(self.stock_name_spinner)

        # Create a text field for Quantity
        self.quantity_input = MDTextField(
            hint_text="Quantity",
            helper_text="Enter Quantity",
            helper_text_mode="on_focus",
        )
        layout.add_widget(self.quantity_input)

        # Create a button to open the date picker
        date_picker_button = MDRaisedButton(
            text="Date",
            pos_hint={'center_x': .5, 'center_y': .6},
            on_release=self.show_date_picker
        )
        layout.add_widget(date_picker_button)

        # Create a text field for Date
        self.date_input = MDTextField(
            hint_text="Date",
            helper_text="Select Date",
            helper_text_mode="on_focus",
            readonly=True
        )
        layout.add_widget(self.date_input)

        # Create a button to open the time picker
        time_picker_button = MDRaisedButton(
            text="Time",
            pos_hint={'center_x': .5, 'center_y': .5},
            on_release=self.show_time_picker
        )
        layout.add_widget(time_picker_button)

        # Create a text field for Time
        self.time_input = MDTextField(
            hint_text="Time",
            helper_text="Select Time",
            helper_text_mode="on_focus",
            readonly=True
        )
        layout.add_widget(self.time_input)

        # Create a button to submit issued items
        submit_button = MDRaisedButton(
            text="Submit",
            pos_hint={"center_x": 0.5},
            on_release=self.submit_stock_issued,
        )
        layout.add_widget(submit_button)

        # Create a button to go back to Home
        back_button = MDRaisedButton(
            text="Back to Home",
            pos_hint={"center_x": 0.5},
            on_release=self.goto_home,
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

    def show_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save, on_cancel=self.on_cancel)
        time_dialog.open()

    def on_time_save(self, instance, value):
        # Format the time value as a string and set it in the time input field
        self.time_input.text = value.strftime('%H:%M:%S')

    def populate_stock_name_spinner(self):
        # Retrieve the list of stock names from the 'stock_inventory' table
        self.cursor.execute('SELECT DISTINCT stock FROM stock_inventory')
        stock = [item[0] for item in self.cursor.fetchall()]

        # Populate the spinner with product names
        self.stock_name_spinner.values = stock

    def submit_stock_issued(self, *args):
        # Get data from input fields
        ccr_name = self.ccr_name_input.text
        stock = self.stock_name_spinner.text  # Retrieve the selected product name from the Spinner
        quantity_str = self.quantity_input.text
        date = self.date_input.text
        time = self.time_input.text

        # Check if all required fields are provided
        if not ccr_name or not stock or not quantity_str or not date:
            self.show_snackbar(text="Please fill in all fields.")
            return

        try:
            # Convert quantity to an integer
            quantity = int(quantity_str)

            # Check if the selected product exists in the inventory
            self.cursor.execute('SELECT quantity FROM stock_inventory WHERE stock = ?', (stock,))
            result = self.cursor.fetchone()

            if result is not None:
                available_quantity = result[0]

                # Check if there is enough quantity available for issuing
                if quantity > available_quantity:
                    self.show_snackbar(text=f"Insufficient quantity available for '{stock}'.")
                    return

                # Subtract the issued quantity from the available quantity
                new_quantity = available_quantity - quantity

                # Update the inventory with the new quantity
                self.cursor.execute('UPDATE stock_inventory SET quantity = ? WHERE stock = ?',
                                    (new_quantity, stock))
                self.conn.commit()

                # Insert the issued item into the 'issuedto' table
                self.cursor.execute(
                    'INSERT INTO stock_issued  (ccr_name, stock, quantity, date, time) VALUES (?, ?, ?, ?, ?)',
                    (ccr_name, stock, quantity, date, time))
                self.conn.commit()

                # Provide feedback to the user, e.g., clear input fields
                self.ccr_name_input.text = ""
                self.stock_name_spinner.text = "Select Stock"  # Reset the selected product name
                self.quantity_input.text = ""
                self.date_input.text = ""
                self.time_input.text = ""

                # Display a Snackbar notification or other feedback
                self.show_snackbar(text="Issued items submitted successfully!")
            else:
                self.show_snackbar(text=f"Product '{stock}' not found in inventory.")
        except ValueError:
            self.show_snackbar(text="Please enter a valid quantity as a positive integer.")

    def goto_home(self, *args):
        self.manager.current = 'home'

    def refresh_stock_list(self, instance):
        # This method will be called when the "Refresh Stock List" button is pressed
        self.populate_stock_name_spinner()

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.date_input.text = value.strftime('%Y-%m-%d')

    def show_snackbar(self, text):
        # Modify Snackbar position to the middle of the screen
        snackbar = Snackbar(text=text, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint_x=None, width=dp(300))
        snackbar.open()

    def on_cancel(self, instance, value):
        pass


stock_names = [
    "Oraimo Charger",
    "Type C to C Charger",
    "Type C to USB Charger",
    "Type C Explore",
    "Iphone X charger",
    "Iphone USB",
    "Shplus Charger",
    "Infinix CA charger",
    "Solar Fan New",
    "MIFI",
    "Smart 7 plus 64-4+3GB",
    "Solar Orbit fan",
    "Solar Adapter AC",
    "Hynet CAT4",
    "itel 5606",
    "Redmi A2+ 32+2",
    "A02",
    "MTN Hynetflex",
    "OALE 2160",
    "MTN PPSK",
    "Redmi A2+ 64+3",
    "solar bulb",
    "MTN Router Deskphone",
    "MTN Smartphone A23",
    "MTN Smartphone A23",
    "A07",
    "Solar bulb",
    "Solar Bulb LED",
    "Solar Inverter",
    "Itel 2163",
    "Lumos Fan",
    "Solar TV Cable",
    "Solar Bulb LED",
    "solar ware",
    "Tecno T101",
    "Redmi 12C 32+3",
    "Tecno T352",
    "ITEL 5636",
    "Vital Phone",
    "TECNO T101",
    "Z Laptop Charger",
    "Z Lufen Deskphone",
    "Z Oale Apex 3",
    "DC Solar Fan",
    "TECNO T101",
    "M1",
    "Redmi 12C 128+4",
    "Extra bass Air peace",
    "Smart 7plus 64+2+2",
    "Sam 1 Airpeace",
    "HOT 20i 64-4GB",
    "Y38 Air peace",
    "H-mobile 5260",
    "PPWB",
    "D-Light",
    "Logical",
    "VTU",
    "MOMO",
    "Others"
]


class StockReturnedHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(StockReturnedHistoryScreen, self).__init__(**kwargs)
        self.data_table = None  # Initialize the MDDataTable
        self.populate_history()

    def populate_history(self, *args):
        # Fetch data from the stock_returned_history table
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS stock_returned_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock TEXT,
                ccr_name TEXT,
                quantity INTEGER,
                date TEXT,
                time TEXT
            )
        ''')

        c.execute('''
            SELECT stock, ccr_name, quantity, date, time
            FROM stock_returned_history
            ORDER BY id DESC  
        ''')
        data = c.fetchall()
        conn.close()

        # Create a FloatLayout to manage widget positioning
        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)

        # Create a new MDDataTable
        column_data = [
            ("Stock", dp(30)),
            ("CCR Name", dp(30)),
            ("Quantity", dp(30)),
            ("Date", dp(30)),
            ("Time", dp(30)),
        ]
        data_table = MDDataTable(check=True, column_data=column_data, rows_num=len(data) + 1)

        # Add data to the new table
        for row in data:
            data_table.add_row(row)

        # Add the new data table to the layout
        layout.add_widget(data_table)

        refresh_button = MDRaisedButton(
            text='Refresh',
            pos_hint={'center_x': .5},
            on_release=self.populate_history
        )
        layout.add_widget(refresh_button)

        back_button = MDRaisedButton(
            text='Back Home',
            pos_hint={'center_x': .5},
            on_release=self.back_to_home
        )
        layout.add_widget(back_button)

        # Clear the old data table (if it exists)
        if self.data_table is not None:
            layout.remove_widget(self.data_table)
            self.data_table = None

        # Add the new layout to the screen
        self.add_widget(layout)

    def back_to_home(self, instance):
        # Navigate back to the home screen
        self.manager.current = 'home'


class StockHistoryTableScreen(Screen):
    def __init__(self, **kwargs):
        super(StockHistoryTableScreen, self).__init__(**kwargs)
        self.data_table = None  # Initialize the MDDataTable
        self.load_stock_history_data()

    def load_stock_history_data(self, *args):
        # Fetch stock history data from the stock_history_table
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS stock_history_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stock TEXT,
                        quantity INTEGER,
                        old_purchase_price INTEGER,
                        old_selling_price INTEGER,
                        new_purchase_price INTEGER,
                        new_selling_price INTEGER,
                        date_added TEXT,
                        serial_no TEXT
                    )
                ''')
        c.execute('''
            SELECT stock, quantity, old_purchase_price, old_selling_price, new_purchase_price, 
            new_selling_price, date_added, serial_no
            FROM stock_history_table
            ORDER BY id DESC
        ''')
        stock_history_data = c.fetchall()
        conn.close()

        # Create a FloatLayout to manage widget positioning
        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)

        # Create a new MDDataTable
        column_data = [
            ("Stock", dp(40)),
            ("Quantity", dp(20)),
            ("Old Purchase Price", dp(30)),
            ("Old Selling Price", dp(30)),
            ("New Purchase Price", dp(30)),
            ("New Selling Price", dp(30)),
            ("Date Added", dp(30)),
            ("Serial No.", dp(30)),
        ]
        data_table = MDDataTable(check=True, column_data=column_data, rows_num=len(stock_history_data) + 1)

        # Add data to the new table
        for row in stock_history_data:
            data_table.add_row(row)

        # Add the new data table to the layout
        layout.add_widget(data_table)

        refresh_button = MDRaisedButton(
            text='Refresh',
            pos_hint={'center_x': .5},
            on_release=self.load_stock_history_data
        )
        layout.add_widget(refresh_button)

        back_button = MDRaisedButton(
            text='Back',
            pos_hint={'center_x': .5},
            on_release=self.back_to_home
        )
        layout.add_widget(back_button)

        # Clear the old data table (if it exists)
        if self.data_table is not None:
            layout.remove_widget(self.data_table)
            self.data_table = None

        # Add the new layout to the screen
        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'


class StockIssuedHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(StockIssuedHistoryScreen, self).__init__(**kwargs)
        self.load_table()

    def load_table(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        # Fetch data from the stock_issued table in LIFO order
        c.execute("SELECT ccr_name, stock, quantity, date, time FROM stock_issued ORDER BY id DESC")
        data = c.fetchall()
        conn.close()

        # Define column names and data
        column_data = [
            ("CCR Name", dp(50)),
            ("Product Name", dp(30)),
            ("Quantity", dp(20)),
            ("Date", dp(25)),
            ("Time", dp(30)),
        ]

        self.table = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=column_data,
            row_data=data,
            check=True,
            rows_num=999999,
        )

        # Create a back button
        back_button = MDRaisedButton(
            text="Back",
            pos_hint={'center_x': .5},
            size_hint=(None, None),
            size=(150, 48)
        )
        back_button.bind(on_release=self.back_to_previous_screen)

        # Create a refresh button
        refresh_button = MDRaisedButton(
            text="Refresh",
            pos_hint={'center_x': .5},
            size_hint=(None, None),
            size=(150, 48)
        )
        refresh_button.bind(on_release=self.refresh_table)

        # Create a layout for the button and the table
        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)
        layout.add_widget(back_button)
        layout.add_widget(refresh_button)
        layout.add_widget(self.table)
        self.add_widget(layout)

    def refresh_table(self, instance):
        # This method will be called when the "Refresh" button is pressed
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        # Fetch data from the stock_issued table
        c.execute("SELECT ccr_name, stock, quantity, date, time FROM stock_issued ORDER BY id DESC")
        data = c.fetchall()
        conn.close()

        self.table.row_data = data

    def back_to_previous_screen(self, instance):
        self.manager.current = 'home'


class SellingPriceScreen(Screen):
    def __init__(self, **kwargs):
        super(SellingPriceScreen, self).__init__(**kwargs)
        self.stock_spinner = Spinner(
            values=[],
            size_hint=(None, None),
            size=(250, 48)
        )
        self.refresh_button = MDRaisedButton(
            text="Refresh",
            size_hint=(None, None),
            size=(100, 48),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        self.refresh_button.bind(on_release=self.refresh_stock_list)

        self.load_stock_items()

        # Add the refresh button to the layout
        self.add_widget(self.refresh_button)

    def load_stock_items(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS stock_inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stock TEXT,
                        quantity INTEGER,
                        new_purchase_price INTEGER,
                        new_selling_price INTEGER,
                        serial_no TEXT
                    )
                ''')

        # Fetch stock items from the stock_inventory table
        c.execute("SELECT stock FROM stock_inventory")
        stock_items = [row[0] for row in c.fetchall()]

        conn.close()

        if not stock_items:
            # Handle the case where there are no stock items
            self.add_widget(MDLabel(text="No stock items available."))
            return

        self.stock_spinner = Spinner(
            text=stock_items[0],  # Default to the first item
            values=stock_items,
            pos_hint={'center_x': .5},
            size_hint=(None, None),
            size=(250, 48),
        )

        self.new_selling_price = MDTextField(
            hint_text="Enter New Selling Price",
            multiline=False,
            input_type='number'
        )

        layout = BoxLayout(orientation='vertical', spacing=12, padding=24)
        layout.add_widget(self.stock_spinner)  # Use self.stock_spinner
        layout.add_widget(self.new_selling_price)

        update_button = MDRaisedButton(
            text='Update',
            size_hint_x=None,
            width=200,
            pos_hint={'center_x': .5},
            on_release=self.update_price,
        )
        layout.add_widget(update_button)

        back_button = MDRaisedButton(
            text='Back To Home',
            size_hint_x=None,
            width=200,
            pos_hint={'center_x': .5},
            on_release=self.back_to_home,
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

        self.stock_spinner.text = "Select Stock"  # Set the Spinner text after deletion

    def update_price(self, instance):
        selected_stock = self.stock_spinner.text
        new_selling_price_text = self.new_selling_price.text

        if not selected_stock or not new_selling_price_text:
            self.show_snackbar("Please fill in all fields.")
            return

        try:
            new_selling_price = int(new_selling_price_text)
        except ValueError:
            self.show_snackbar("Selling price must be a valid number.")
            return

        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('''
            UPDATE stock_inventory
            SET new_selling_price = ?
            WHERE stock = ?
        ''', (new_selling_price, selected_stock))
        conn.commit()
        conn.close()

        self.show_snackbar("Selling price updated successfully")
        self.stock_spinner.text = "Select Stock"
        self.new_selling_price.text = ""

    def show_snackbar(self, text):
        snackbar = Snackbar(text=text, pos_hint={'center_x': .5, 'center_y': .5}, size_hint_x=None, width=dp(300))
        snackbar.open()

    def refresh_stock_list(self, instance):
        # Refresh the stock list in the Spinner
        self.load_stock_items()

    def back_to_home(self, instance):
        self.manager.current = 'home'


class NewDawnInventoryApp(MDApp):
    selected_stock = StringProperty("")  # Define the selected_stock property

    def set_selected_stock(self, stock):
        self.selected_stock = stock

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls_accent_hue = '400'

        self.conn = sqlite3.connect('user_data.db')
        self.create_table()

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddStockScreen(name='add_stock'))  # Add the AddStockScreen
        sm.add_widget(ReturnedStockScreen(name='returned_stock'))  # Add this line
        sm.add_widget(ViewInventoryScreen(name='view_inventory_data'))
        sm.add_widget(DeleteStockScreen(name='delete_stock'))
        sm.add_widget(StockIssuedScreen(name='stock_issued'))
        sm.add_widget(StockReturnedHistoryScreen(name='stock_returned_history'))
        sm.add_widget(StockHistoryTableScreen(name='stock_history_table'))
        sm.add_widget(StockIssuedHistoryScreen(name='stock_issued_history'))
        sm.add_widget(SellingPriceScreen(name='selling_price'))

        return sm

    def set_selected_stock(self, stock_name):
        self.selected_stock = stock_name

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (role TEXT, username TEXT, password TEXT, phone TEXT, email TEXT)''')
        self.conn.commit()

    def on_stop(self):
        self.conn.close()


if __name__ == '__main__':
    NewDawnInventoryApp().run()
