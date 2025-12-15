import frappe
from frappe import _
from frappe.model.naming import append_number_if_name_exists
from frappe.utils import escape_html, random_string
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
    # Skip if user was created via SQL (role already exists)
    # This prevents triggering save/on_update which would send emails
    if frappe.db.exists("Has Role", {"parent": doc.name, "role": "LMS Student"}) or \
       frappe.db.exists("Has Role", {"parent": doc.name, "role": "Course Creator"}):
        # User was created via SQL, role already added, skip to avoid triggering save
        return

    # Only add role if it doesn't already exist and user was created via Document model
    existing_roles = [d.role for d in doc.get("roles", [])]
    # Default to LMS Student if no role exists
    if "LMS Student" not in existing_roles and "Course Creator" not in existing_roles:
        # Set flags to prevent email sending
        doc.flags.email_sent = 1
        doc.flags.no_welcome_mail = True
        doc.add_roles("LMS Student")


@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, verify_terms, user_category, user_type="student"):
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

    # Create new User using direct SQL insertion to completely bypass Document model and email hooks
    user_name = email.strip().lower()
    first_name_escaped = escape_html(full_name)
    from frappe.utils import now_datetime, get_system_timezone
    from frappe.utils.password import passlibctx

    now = now_datetime()
    time_zone = get_system_timezone()
    user = None

    try:
        # Insert user directly using SQL to bypass all hooks
        # Set send_welcome_email=0 explicitly to prevent email sending
        frappe.db.sql("""
            INSERT INTO `tabUser` (
                name, email, first_name, full_name, enabled,
                send_welcome_email, user_type, country, time_zone,
                creation, modified, owner, modified_by, docstatus, idx
            ) VALUES (
                %s, %s, %s, %s, %s,
                0, %s, %s, %s,
                %s, %s, %s, %s, 0, 0
            )
        """, (
            user_name, user_name, first_name_escaped, first_name_escaped, 1,
            "Website User", "", time_zone,
            now, now, "Administrator", "Administrator"
        ))

        # Immediately update send_welcome_email to 0 again in case anything changed it
        # This ensures no welcome email is sent even if document is loaded later
        frappe.db.sql("""
            UPDATE `tabUser`
            SET send_welcome_email = 0
            WHERE name = %s
        """, (user_name,))

        frappe.log_error(
            f"[user.py] (User inserted into DB via SQL: {user_name})", "LMS Signup Debug")

        # Set password hash directly in __Auth table using SQL
        hashPwd = passlibctx.hash("123123")

        if frappe.db.db_type == "mariadb":
            frappe.db.sql("""
                INSERT INTO `__Auth` (doctype, name, fieldname, password, encrypted)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE password = %s, encrypted = %s
            """, ("User", user_name, "password", hashPwd, 0, hashPwd, 0))
        elif frappe.db.db_type == "postgres":
            frappe.db.sql("""
                INSERT INTO "__Auth" (doctype, name, fieldname, password, encrypted)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (doctype, name, fieldname)
                DO UPDATE SET password = %s, encrypted = %s
            """, ("User", user_name, "password", hashPwd, 0, hashPwd, 0))

        frappe.log_error(
            f"[user.py] (Password set for user: {user_name})", "LMS Signup Debug")

        # Create notification settings using SQL (normally done in after_insert hook)
        if not frappe.db.exists("Notification Settings", user_name):
            frappe.db.sql("""
                INSERT INTO `tabNotification Settings` (
                    name, creation, modified, owner, modified_by, docstatus, idx
                ) VALUES (
                    %s, %s, %s, %s, %s, 0, 0
                )
            """, (user_name, now, now, "Administrator", "Administrator"))

        # Add role based on user type (Student or Teacher)
        role_name = frappe.generate_hash(length=10)
        # Determine role: "Course Creator" for teachers, "LMS Student" for students
        role = "Course Creator" if user_type.lower() == "teacher" else "LMS Student"
        frappe.db.sql("""
            INSERT INTO `tabHas Role` (
                name, parent, parenttype, parentfield, role,
                creation, modified, owner, modified_by, docstatus, idx
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, 0, 0
            )
        """, (
            role_name, user_name, "User", "roles", role,
            now, now, "Administrator", "Administrator"
        ))

        frappe.log_error(
            f"[user.py] (Role '{role}' added to user: {user_name})", "LMS Signup Debug")

        # Set country from IP using SQL (avoid any document operations)
        country_code = get_country_code()
        if country_code:
            frappe.db.sql("""
                UPDATE `tabUser`
                SET country = %s
                WHERE name = %s AND (country IS NULL OR country = '')
            """, (country_code, user_name))

        # Clear cache
        frappe.cache.delete_key("users_for_mentions")
        frappe.cache.delete_key("enabled_users")

        # Commit transaction
        frappe.db.commit()

        # Don't load User doc to avoid triggering any hooks
        # Just use user_name string for subsequent operations
        user = user_name

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
        f"[user.py] (User fully created: {user}, returning success message)", "LMS Signup Debug")

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
