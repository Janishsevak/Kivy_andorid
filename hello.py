from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from kivy.uix.gridlayout import GridLayout

# Firebase Setup
cred = credentials.Certificate(r"F:\Mobile\firstapp-a74b4-firebase-adminsdk-annkl-e9ff32bc11.json")  # Update with your Firebase credentials
initialize_app(cred)
db = firestore.client()

# Firebase Collection Names
USERS_COLLECTION = "Users"
LOAN_COLLECTION = "Loans"

# KV Code
KV = '''
ScreenManager:
    LoginScreen:
    UserScreen:
    LoanApplicationScreen:
    GuaranteeRequestScreen:
    AdminScreen:
    LoanStatusScreen:

<LoginScreen>:
    name: "login"  # This should be part of the screen definition
    FloatLayout:
        Image:
            source: "F:\Mobile\download.jfif"  # Path to your image
            allow_stretch: True  # Ensure the image stretches to fill the screen
            keep_ratio: False  # Ignore the aspect ratio for full screen coverage
            size: self.size  # Match the screen size
            pos: self.pos  # Match the screen position

        BoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 10
            size_hint: 0.8, 0.5  # Adjust the size of the BoxLayout
            pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the BoxLayout
            Label:
                text: "Welcome to Surat Society"
                font_size: "50sp"
                color: 1, 0, 0, 1
            TextInput:
                id: email_field
                hint_text: "Enter Email"
                multiline: False
                size_hint: 0.4, None  # 80% width of the parent, and height is explicitly set
                height: "40dp"  # Set a fixed height
                pos_hint: {"center_x": 0.5}  # Center horizontally
            TextInput:
                id: password_field
                hint_text: "Enter Password"
                password: True
                multiline: False
                size_hint: 0.4, None  # 80% width of the parent, and height is explicitly set
                height: "40dp"  # Set a fixed height
                pos_hint: {"center_x": 0.5}
            Button:
                text: "Login"
                on_press: app.login(email_field.text, password_field.text)
                size_hint: 0.2, None  # 80% width of the parent, and height is explicitly set
                height: "40dp"  # Set a fixed height
                pos_hint: {"center_x": 0.5}
<UserScreen>:
    name: "user"
    FloatLayout:
        Image:
            source: "F:\Mobile\download.jfif"  # Replace with your background image path
            allow_stretch: True
            keep_ratio: False
            size: self.size
            pos: self.pos

        BoxLayout:
            orientation: "vertical"
            size_hint: None, None
            size: 600, 500
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

            GridLayout:
                cols: 2
                spacing: 20
                size_hint: 1, 1

                # Add Data Section
                BoxLayout:
                    orientation: "vertical"
                    spacing: 10
                    size_hint: None, None
                    size: 150, 150

                    Image:
                        source: "F:\Mobile\data_add.png"  # Replace with your icon path
                        size_hint: None, None
                        size: 100, 100

                    Button:
                        text: "Add Data"
                        size_hint: None, None
                        size: 100, 40
                        on_press: app.add_data()

                # Apply Loan Section
                BoxLayout:
                    orientation: "vertical"
                    spacing: 10
                    size_hint: None, None
                    size: 150, 150

                    Image:
                        source: "F:\Mobile\Reason-to-Apply-for-a-Personal-Loan.jpg"  # Replace with your icon path
                        size_hint: None, None
                        size: 100, 100

                    Button:
                        text: "Apply Loan"
                        size_hint: None, None
                        size: 100, 40
                        on_press: app.sm.current = "loan_application"

                # Guarantee Requests Section
                BoxLayout:
                    orientation: "vertical"
                    spacing: 10
                    size_hint: None, None
                    size: 150, 150

                    Image:
                        source: "F:\Mobile\download.png"  # Replace with your icon path
                        size_hint: None, None
                        size: 100, 100

                    Button:
                        text: "Requests"
                        size_hint: None, None
                        size: 100, 40
                        on_press: app.sm.current = "guarantee_request"

                # Exit Section
                BoxLayout:
                    orientation: "vertical"
                    spacing: 10
                    size_hint: None, None
                    size: 150, 150

                    Image:
                        source: "F:\Mobile\exit.png"  # Replace with your icon path
                        size_hint: None, None
                        size: 100, 100

                    Button:
                        text: "Logout"
                        size_hint: None, None
                        size: 100, 40
                        on_press: app.logout()



<LoanApplicationScreen>:
    name: "loan_application"
    FloatLayout:
        Image:
            source: "F:\Mobile\download.jfif"  # Path to your image
            allow_stretch: True  # Ensure the image stretches to fill the screen
            keep_ratio: False  # Ignore the aspect ratio for full screen coverage
            size: self.size  # Match the screen size
            pos: self.pos  # Match the screen position

    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        Label:
            text: "Loan Application Form"
            font_size: "24sp"

        TextInput:
            id: loan_reason
            hint_text: "Reason for Loan"

        TextInput:
            id: loan_amount
            hint_text: "Loan Amount"

        Spinner:
            id: guarantor1
            text: "Select First Guarantor"
            values: []
            on_text: root.update_guarantor2_values(self.text)  # Ensure proper argument is passed

        Spinner:
            id: guarantor2
            text: "Select Second Guarantor"
            values: []

        Button:
            text: "Submit Loan Application"
            on_press: app.submit_loan(loan_reason.text, loan_amount.text, guarantor1.text, guarantor2.text)

        Button:
            text: "Back"
            on_press: app.sm.current = "user"



<GuaranteeRequestScreen>:
    name: "guarantee_request"
    BoxLayout:
        orientation: "vertical"
        padding: [10, 10, 10, 10]
        spacing: 5

        Label:
            text: "Pending Requests"
            font_size: "18sp"
            size_hint_y: None
            height: 30

        ScrollView:
            size_hint: (1, 1)
            GridLayout:
                id: pending_requests_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 2
                padding: [5, 0, 5, 0]

        Label:
            text: "Your Responses"
            font_size: "18sp"
            size_hint_y: None
            height: 30  # Minimal height for the label

        ScrollView:
            size_hint_y: None
            height: self.parent.height * 0.4  # Adjusted to use a proportion of available height
            do_scroll_x: False
            do_scroll_y: True
            GridLayout:
                id: responded_requests_table
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
                padding: [5, 0, 5, 0]  # Small padding around the table for alignment

        Button:
            text: "Back"
            size_hint: None, None
            size: 100, 50
            pos_hint: {"center_x": 0.5}
            on_press: app.sm.current = "user"



<AdminScreen>:
    name: "admin"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10
        Button:
            text: "Loan Status"
            on_press: app.sm.current = "loan_status"
        Button:
            text: "Logout"
            on_press: app.logout()

<LoanStatusScreen>:
    name: "loan_status"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10
        Label:
            text: "Loan Status"
            font_size: "24sp"
        ScrollView:
            GridLayout:
                id: loan_status_list
                cols: 7
                size_hint_y: None
                height: self.minimum_height
        Button:
            text: "Back"
            size_hint_y: None
            height: 40
            on_press: app.sm.current = "admin"
'''

# Screen Definitions
class LoginScreen(Screen):
    pass

class UserScreen(Screen):
    pass

class LoanApplicationScreen(Screen):
    def on_pre_enter(self, *args):
        """Populate the guarantor dropdowns when the screen is entered."""
        app = App.get_running_app()
        self.populate_guarantors(app.current_user["email"])

    def populate_guarantors(self, current_user_email):
        """Fetch and display available guarantors in the dropdown menus."""
        try:
            # Fetch non-admin users from the database
            users = db.collection(USERS_COLLECTION).where("is_admin", "==", False).get()

            # Filter out the current user
            guarantor_list = [user.to_dict()["email"] for user in users if user.to_dict()["email"] != current_user_email]

            # Populate dropdowns with the filtered list
            self.ids.guarantor1.values = guarantor_list
            self.ids.guarantor2.values = guarantor_list

            # Reset dropdowns
            self.ids.guarantor1.text = "Select First Guarantor"
            self.ids.guarantor2.text = "Select Second Guarantor"

        except Exception as e:
            # Show error popup in case of failure
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to load guarantors: {e}")

    def update_guarantor2_values(self, selected_value=None):
        """Update the options in guarantor2 dropdown based on the selection in guarantor1."""
        try:
            # Get the original list of guarantors
            all_guarantors = self.ids.guarantor1.values

            # Filter out the selected value from guarantor1
            filtered_guarantors = [guarantor for guarantor in all_guarantors if guarantor != selected_value]

            # Update guarantor2 dropdown values
            self.ids.guarantor2.values = filtered_guarantors

            # Reset guarantor2 dropdown if its current value is filtered out
            if self.ids.guarantor2.text not in filtered_guarantors:
                self.ids.guarantor2.text = "Select Second Guarantor"

        except Exception as e:
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to update guarantor options: {e}")



class GuaranteeRequestScreen(Screen):
    def on_pre_enter(self, *args):
        """Populate both pending requests and responded requests."""
        app = App.get_running_app()
        self.populate_pending_requests(app.current_user["email"])
        self.populate_responded_requests(app.current_user["email"])

    def populate_pending_requests(self, current_user_email):
        """Populate pending guarantee requests in a table format."""
        try:
            # Fetch loan requests where the current user is a guarantor
            requests = db.collection(LOAN_COLLECTION).where("guarantors", "array_contains", current_user_email).get()

            # Clear existing widgets in the list
            request_list = self.ids.pending_requests_list
            request_list.clear_widgets()

            # Filter requests where the user hasn't responded yet
            pending_requests = [
                req for req in requests
                if req.to_dict()["guarantor_responses"].get(current_user_email) is None
            ]

            # If no pending requests, show a message
            if not pending_requests:
                request_list.add_widget(Label(text="No pending requests.", size_hint_y=None, height=40))
                return
            # Create a header row for the table
            header = GridLayout(cols=5, size_hint_y=None, height=40, spacing=10)
            equal_width = 0.2   # Define column widths
            # Add a header row
            header.add_widget(Label(text="Applicant", size_hint_x=equal_width, bold=True, font_size="14sp"))
            header.add_widget(Label(text="Reason", size_hint_x=equal_width, bold=True, font_size="14sp"))
            header.add_widget(Label(text="Amount", size_hint_x=equal_width, bold=True, font_size="14sp"))
            header.add_widget(Label(text="Approve", size_hint_x=equal_width, bold=True, font_size="14sp"))
            header.add_widget(Label(text="Reject", size_hint_x=equal_width, bold=True, font_size="14sp"))
            request_list.add_widget(header)

            # Add each pending request as a row
            for request in pending_requests:
                data = request.to_dict()

                # Get details
                applicant = data.get("applicant", "Unknown")
                reason = data.get("reason", "Unknown")
                amount = data.get("amount", "Unknown")

                # Create a row
                row = GridLayout(cols=5, size_hint_y=None, height=40, spacing=5)

                # Add request details
                row.add_widget(Label(text=applicant, size_hint_x=equal_width, font_size="12sp"))
                row.add_widget(Label(text=reason, size_hint_x=equal_width, font_size="12sp"))
                row.add_widget(Label(text=str(amount), size_hint_x=equal_width, font_size="12sp"))

                # Add Approve button
                approve_button = Button(text="Approve", size_hint_x=equal_width, font_size="12sp")
                approve_button.bind(on_press=lambda btn, doc_id=request.id: self.respond_to_request(doc_id, True))
                row.add_widget(approve_button)

            # Add Reject button
                reject_button = Button(text="Reject", size_hint_x=equal_width, font_size="12sp")
                reject_button.bind(on_press=lambda btn, doc_id=request.id: self.respond_to_request(doc_id, False))
                row.add_widget(reject_button)

                # Add the row to the request list
                request_list.add_widget(row)

        except Exception as e:
            # Show an error popup in case of failure
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to load pending requests: {e}")


    def populate_responded_requests(self, current_user_email):
        """Populate a table of responded requests."""
        try:
            # Fetch all requests where the user is a guarantor
            requests = db.collection(LOAN_COLLECTION).where("guarantors", "array_contains", current_user_email).get()

            # Clear the table
            responded_requests = [
            req.to_dict() for req in requests
            if req.to_dict()["guarantor_responses"].get(current_user_email) is not None
        ]

        # Sort requests by date (assuming 'date' is stored in ISO 8601 or timestamp format)
            responded_requests.sort(key=lambda x: x.get("date", ""), reverse=True)  # Latest date first

        # Clear existing widgets in the table
            response_table = self.ids.responded_requests_table
            response_table.clear_widgets()

             # Add a message if no responded requests are found
            if not responded_requests:
               response_table.add_widget(Label(text="No responses found.", size_hint_y=None, height=40))
               return
             # Define column widths (to ensure alignment)
            column_widths = [100, 150, 100, 100, 120]
        # Create a header row for the table
            header = GridLayout(cols=5, size_hint_y=None, height=40, spacing=10)
            header.add_widget(Label(text="Applicant", size_hint=(None, 1), width=column_widths[0], font_size="14sp", bold=True))
            header.add_widget(Label(text="Reason", size_hint=(None, 1), width=column_widths[1], font_size="14sp", bold=True))
            header.add_widget(Label(text="Amount", size_hint=(None, 1), width=column_widths[2], font_size="14sp", bold=True))
            header.add_widget(Label(text="Response", size_hint=(None, 1), width=column_widths[3], font_size="14sp", bold=True))
            header.add_widget(Label(text="Date", size_hint=(None, 1), width=column_widths[4], font_size="14sp", bold=True))
            response_table.add_widget(header)


           

        # Add each responded request to the table
            for data in responded_requests:
               applicant = str(data.get("applicant", "Unknown"))
               reason = str(data.get("reason", "Unknown"))
               amount = str(data.get("amount", "Unknown"))
               response = str(data["guarantor_responses"].get(current_user_email, "Unknown"))
               date = str(data.get("date", "Unknown"))
            # Create a row for the table
               row = GridLayout(cols=5, size_hint_y=None, height=40, spacing=10)

            # Add details to the row
               row.add_widget(Label(text=applicant, size_hint=(None, 1), width=column_widths[0], font_size="12sp"))
               row.add_widget(Label(text=reason, size_hint=(None, 1), width=column_widths[1], font_size="12sp"))
               row.add_widget(Label(text=amount, size_hint=(None, 1), width=column_widths[2], font_size="12sp"))
               row.add_widget(Label(text=response, size_hint=(None, 1), width=column_widths[3], font_size="12sp"))
               row.add_widget(Label(text=date, size_hint=(None, 1), width=column_widths[4], font_size="12sp"))

            # Add the row to the table
               response_table.add_widget(row)

        except Exception as e:
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to load responded requests: {e}")

    def respond_to_request(self, loan_id, approved):
        """Update the response for the loan request."""
        try:
            app = App.get_running_app()

            # Fetch the loan document
            loan_ref = db.collection(LOAN_COLLECTION).document(loan_id)
            loan_data = loan_ref.get().to_dict()

            # Update the user's response
            loan_data["guarantor_responses"][app.current_user["email"]] = "approved" if approved else "rejected"

            # Update loan status based on responses
            if all(resp == "approved" for resp in loan_data["guarantor_responses"].values()):
                loan_data["approved"] = True
            elif any(resp == "rejected" for resp in loan_data["guarantor_responses"].values()):
                loan_data["approved"] = False

            # Save the changes
            loan_ref.update(loan_data)
            app.show_popup("Success", "Your response has been recorded.")
            self.on_pre_enter()  # Refresh the screen
        except Exception as e:
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to respond to request: {e}")






class AdminScreen(Screen):
    pass

class LoanStatusScreen(Screen):
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.populate_loan_status()

    def populate_loan_status(self):
        try:
            loans = db.collection(LOAN_COLLECTION).get()

            # Clear existing widgets
            loan_status_list = self.ids.loan_status_list
            loan_status_list.clear_widgets()

            # Add table headers
            headers = ["Date", "Applicant", "Amount", "Guarantor 1", "Guarantor 1 Status", "Guarantor 2", "Guarantor 2 Status"]
            for header in headers:
                loan_status_list.add_widget(Label(text=header, bold=True, size_hint_y=None, height=40))

            # Populate table rows with loan data
            for loan in loans:
                data = loan.to_dict()

                # Safely retrieve values
                date = str(data.get("date", "N/A"))
                applicant = str(data.get("applicant", "N/A"))
                amount = str(data.get("amount", "N/A"))
                guarantors = data.get("guarantors", ["N/A", "N/A"])
                guarantor1 = str(guarantors[0]) if len(guarantors) > 0 else "N/A"
                guarantor2 = str(guarantors[1]) if len(guarantors) > 1 else "N/A"
                responses = data.get("guarantor_responses", {})

                # Handle guarantor statuses with a default of "Pending"
                guarantor1_status = responses.get(guarantor1, "Pending")
                guarantor2_status = responses.get(guarantor2, "Pending")

                # Ensure all values are strings for the Label widget
                guarantor1_status = str(guarantor1_status if guarantor1_status is not None else "Pending")
                guarantor2_status = str(guarantor2_status if guarantor2_status is not None else "Pending")

                # Add rows to the table
                loan_status_list.add_widget(Label(text=date, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=applicant, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=amount, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=guarantor1, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=guarantor1_status, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=guarantor2, size_hint_y=None, height=40))
                loan_status_list.add_widget(Label(text=guarantor2_status, size_hint_y=None, height=40))
        except Exception as e:
            app = App.get_running_app()
            app.show_popup("Error", f"Failed to load loan status: {e}")






class DataEntryApp(App):
    current_user = None

    def build(self):
        self.sm = Builder.load_string(KV)
        return self.sm

    def login(self, email, password):
        try:
            user_ref = db.collection(USERS_COLLECTION).where("email", "==", email).where("password", "==", password).get()
            if user_ref:
                user_data = user_ref[0].to_dict()
                self.current_user = user_data
                self.sm.current = "admin" if user_data.get("is_admin") else "user"
            else:
                self.show_popup("Error", "Invalid credentials!")
        except Exception as e:
            self.show_popup("Error", f"Login failed: {e}")

    def logout(self):
        self.current_user = None
        self.sm.current = "login"

    def submit_loan(self, reason, amount, guarantor1, guarantor2):
        try:
            loan_data = {
                "applicant": self.current_user["email"],
                "reason": reason,
                "amount": amount,
                "guarantors": [guarantor1, guarantor2],
                "approved": False,
                "guarantor_responses": {guarantor1: None, guarantor2: None},
                "date": datetime.now().strftime("%Y-%m-%d"),
                "approved_date": None,
                "rejected_date": None,
            }
            db.collection(LOAN_COLLECTION).add(loan_data)
            self.show_popup("Success", "Loan application submitted successfully!")
            self.sm.current = "user"
        except Exception as e:
            self.show_popup("Error", f"Failed to submit loan: {e}")

    def guarantor_response(self, loan_id, approved):
        try:
            loan_ref = db.collection(LOAN_COLLECTION).document(loan_id)
            loan_data = loan_ref.get().to_dict()

            if approved:
                loan_data["guarantor_responses"][self.current_user["email"]] = "approved"
            else:
                loan_data["guarantor_responses"][self.current_user["email"]] = "rejected"

            if all(resp == "approved" for resp in loan_data["guarantor_responses"].values()):
                loan_data["approved"] = True
            elif any(resp == "rejected" for resp in loan_data["guarantor_responses"].values()):
                loan_data["approved"] = False

            loan_ref.update(loan_data)
            self.show_popup("Success", "Response submitted successfully!")
            self.sm.current = "guarantee_request"
        except Exception as e:
            self.show_popup("Error", f"Failed to update response: {e}")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
        )
        popup.open()

    


if __name__ == "__main__":
    DataEntryApp().run()
