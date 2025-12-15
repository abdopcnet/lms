import frappe
from frappe.core.doctype.user.user import User


class CustomUser(User):
    def send_password_notification(self, new_password):
        # Check if user was created via SQL by checking send_welcome_email=0 in DB
        # This prevents email sending for SQL-created users
        db_send_welcome_email = frappe.db.get_value(
            "User", self.name, "send_welcome_email")
        if db_send_welcome_email == 0:
            # User was created via SQL (send_welcome_email=0), prevent email sending
            self.flags.email_sent = 1
            self.flags.no_welcome_mail = True
            # Ensure send_welcome_email is 0 in document
            self.send_welcome_email = 0
            # Skip email sending entirely to prevent OutgoingEmailError
            return

        # Call parent send_password_notification for normal users
        super().send_password_notification(new_password)
