import frappe

# Landing page context - no login required
no_cache = 1


def get_context(context):
    """Get context for the landing page template"""
    # Brand settings
    context.brand_name = frappe.db.get_single_value("Website Settings", "app_name") or "Learning"
    context.brand_logo = frappe.db.get_single_value("Website Settings", "banner_image")
    context.favicon = frappe.db.get_single_value("Website Settings", "favicon") or "/assets/lms/frontend/favicon.png"
    context.title = "Home"

    # User info for logged-in users
    if frappe.session.user != "Guest":
        user = frappe.db.get_value(
            "User",
            frappe.session.user,
            ["full_name", "user_image", "username"],
            as_dict=True
        )
        if user:
            context.full_name = user.full_name
            context.user_image = user.user_image
            context.username = user.username

            # Check user roles
            roles = frappe.get_roles(frappe.session.user)
            context.is_instructor = "Course Creator" in roles
            context.is_moderator = "Moderator" in roles
            context.is_system_user = frappe.db.get_value("User", frappe.session.user, "user_type") == "System User"

    # Get published courses for the popular courses section
    try:
        courses = frappe.get_all(
            "LMS Course",
            filters={"published": 1},
            fields=[
                "name",
                "title",
                "short_introduction",
                "image",
                "paid",
                "course_price",
                "currency"
            ],
            order_by="creation desc",
            limit=6
        )

        # Add instructor info and lesson count
        for course in courses:
            # Get instructor
            instructor = frappe.db.get_value(
                "Course Instructor",
                {"parent": course.name},
                "instructor"
            )
            if instructor:
                course.instructor_name = frappe.db.get_value("User", instructor, "full_name")

            # Get lesson count
            course.lesson_count = frappe.db.count(
                "Course Lesson",
                {"course": course.name}
            )

        context.courses = courses
    except Exception:
        context.courses = []

    return context
