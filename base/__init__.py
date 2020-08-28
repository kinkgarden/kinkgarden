from functools import wraps


def ignore_age_gate(view_func):
    """Mark a view function as being exempt from the CSRF view protection."""
    # view_func.csrf_exempt = True would also work, but decorators are nicer
    # if they don't have side effects, so return a new function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.ignore_age_gate = True
    return wraps(view_func)(wrapped_view)
