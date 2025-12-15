import frappe
from frappe import _
from frappe.model.naming import append_number_if_name_exists
from frappe.website.utils import cleanup_page_name, is_signup_disabled

from lms.lms.utils import get_country_code


def validate_username_duplicates(doc, method):
    while not doc.username or doc.username_exists():
        doc.username = append_number_if_name_exists(
            doc.doctype, cleanup_page_name(doc.full_name), fieldname="username"
        )
    if " " in doc.username:
        doc.username = doc.username.replace(" ", "")

    if len(doc.username) < 4:
        doc.username = doc.email.replace("@", "").replace(".", "")


def after_insert(doc, method):
    # Check if role already exists to avoid duplicate role addition
    existing_roles = [d.role for d in doc.get("roles", [])]

    # Only add default role if no role exists and user was created via sign_up
    # The sign_up function handles role assignment, so this is a fallback
    if "LMS Student" not in existing_roles and "Course Creator" not in existing_roles:
        # Set flags to prevent email sending
        doc.flags.email_sent = 1
        doc.flags.no_welcome_mail = True
        doc.add_roles("LMS Student")


@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, verify_terms, user_category, user_type="student", mobile_no=None):
    frappe.log_error(
        f"[user.py] (Signup started for: {email}, type: {user_type})", "LMS Signup Debug")

    if is_signup_disabled():
        frappe.throw(_("Sign Up is disabled"), _("Not Allowed"))

    user = frappe.db.get("User", {"email": email})
    if user:
        if user.enabled:
            return {
                "success": False,
                "message": _("Already Registered")
            }
        else:
            return {
                "success": False,
                "message": _("Registered but disabled")
            }

    if frappe.db.get_creation_count("User", 60) > 300:
        frappe.respond_as_web_page(
            _("Temporarily Disabled"),
            _(
                "Too many users signed up recently, so the registration is disabled. Please try back in an hour"
            ),
            http_status_code=429,
        )
        return

    frappe.log_error(
        f"[user.py] (Creating new user with enabled=1, password set)", "LMS Signup Debug")

    from frappe.utils import get_system_timezone

    try:
        # Generate username from full_name
        user_name = email.strip().lower()
        username = cleanup_page_name(full_name)
        if " " in username:
            username = username.replace(" ", "")

        # Ensure username is at least 4 characters
        if len(username) < 4:
            username = user_name.replace("@", "").replace(".", "")

        # Check if username exists and append number if needed
        username = append_number_if_name_exists(
            "User", username, fieldname="username")

        # Create new User using frappe.new_doc (follows Frappe best practices)
        user = frappe.new_doc("User")
        user.email = user_name
        user.first_name = full_name  # Frappe handles escaping automatically
        user.enabled = 1
        user.send_welcome_email = 0
        user.user_type = "Website User"
        user.time_zone = get_system_timezone()
        user.username = username

        # Set custom fields
        if mobile_no and mobile_no.strip():
            user.phone = mobile_no.strip()
        if verify_terms:
            user.verify_terms = 1

        # Map user_category to valid Select field options
        # Valid options: "", "Business Owner", "Manager (Sales/Marketing/Customer)",
        # "Employee", "Student", "Freelancer/Just looking", "Others"
        if user_type.lower() == "student":
            user.user_category = "Student"
        elif user_type.lower() == "teacher":
            user.user_category = "Employee"  # Teachers are employees
        elif user_category:
            # If user_category is provided and matches a valid option, use it
            valid_options = ["", "Business Owner", "Manager (Sales/Marketing/Customer)",
                             "Employee", "Student", "Freelancer/Just looking", "Others"]
            if user_category in valid_options:
                user.user_category = user_category
            else:
                # Default to empty if invalid
                user.user_category = ""

        # Set flags to prevent email sending
        user.flags.no_welcome_mail = True
        user.flags.email_sent = 1
        user.flags.ignore_permissions = True
        user.flags.ignore_password_policy = True

        # Insert user (this triggers hooks, but flags prevent email sending)
        user.insert()

        frappe.log_error(
            f"[user.py] (User created via Document model: {user.name})", "LMS Signup Debug")

        # Set password
        user.new_password = "123123"
        user.save()

        frappe.log_error(
            f"[user.py] (Password set for user: {user.name})", "LMS Signup Debug")

        # Add role based on user type (Student or Teacher)
        role = "Course Creator" if user_type.lower() == "teacher" else "LMS Student"
        user.add_roles(role)

        frappe.log_error(
            f"[user.py] (Role '{role}' added to user: {user.name})", "LMS Signup Debug")

        # Set country from IP
        country_code = get_country_code()
        if country_code:
            user.country = country_code
            user.save()

        # Cache is cleared automatically by after_insert hook

    except Exception as e:
        # Log any errors
        frappe.log_error(
            f"[user.py] (Error during insert: {str(e)})", "LMS Signup Error")
        frappe.db.rollback()
        return {
            "success": False,
            "message": _("Registration failed: {0}").format(str(e))
        }

    frappe.log_error(
        f"[user.py] (User fully created: {user.name}, returning success message)", "LMS Signup Debug")

    response = {
        "success": True,
        "message": _("Account created successfully! Your password is: 123123")
    }

    frappe.log_error(
        f"[user.py] (Returning response: {response})", "LMS Signup Debug")

    return response


def set_country_from_ip(login_manager=None, user=None):
    if not user and login_manager:
        user = login_manager.user
    user_country = frappe.db.get_value("User", user, "country")
    if user_country:
        return
    frappe.db.set_value("User", user, "country", get_country_code())
    return


def on_login(login_manager):
    default_app = frappe.db.get_single_value("System Settings", "default_app")
    if default_app == "lms":
        frappe.local.response["home_page"] = "/lms"
