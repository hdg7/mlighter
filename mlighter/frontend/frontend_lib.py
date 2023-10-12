import sys
import os
import ipyvuetify as v
import ipywidgets as widgets


# SESSION
def initialise_session():
    home_value = os.getenv('MLIGHTER_HOME')

    if home_value is None:
        home_value = os.path.join(
            os.getenv('HOME'),
            "mlighter", "mlighter"
        )

    sys.path.append(home_value + "/backend")

    from MLighter import MLighter  # noqa

    session = MLighter({})

    return session


# LOGGING
sys.stdout = open('/dev/stdout', 'w')


def log(string_to_log):
    print(string_to_log, file=sys.stdout)


def log_on_same_line(string_to_log):
    print(string_to_log, file=sys.stdout, end='')


# TESTING
"""
Testing is done with the test button at the bottom of the notebook.
These tests are intended to ensure the system as a whole is functional and are not meant as unit tests.
There is no isolation between tests.
"""
tests_to_run = []


def add_class_test(cls_instance):
    """
    If a class contains tests call this during initialisation if you will construct a class anyway,
    or when you construct a class
    """
    for attr_name in dir(cls_instance):
        attr = getattr(cls_instance, attr_name)
        if hasattr(attr, '__test__') and attr.__test__:
            if attr not in tests_to_run:
                tests_to_run.append(attr)


def mark_test(*args, **kwargs):
    """Decorator to mark a function as a test"""
    def _mark_test(func, test_tag=None, test_name=None):
        if test_tag is not None:
            func.test_tag = test_tag
        if test_name is not None:
            func.test_name = test_name

        func.__test__ = True

        if "." not in func.__qualname__:
            if func not in tests_to_run:
                tests_to_run.append(func)

        return func

    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _mark_test(args[0])
    else:
        return lambda func: _mark_test(func, *args, **kwargs)


def run_tests():
    """Call this to run tests"""
    tests_by_tag = {}
    for test in tests_to_run:
        tag = 'default'
        if hasattr(test, 'test_tag'):
            tag = 'default'

        if tag not in tests_by_tag:
            tests_by_tag[tag] = []
        tests_by_tag[tag].append(test)

    log(f"Running {len(tests_to_run)} tests")

    failures = {}

    for tag, tests in tests_by_tag.items():
        log(f"Running {len(tests)} tests for tag {tag}")
        for test in tests:
            name = test.__qualname__
            if test.__name__ is not None:
                name = test.__name__
            try:
                test()
                log_on_same_line(".")
            except AssertionError as e:
                log_on_same_line("F")
                failures[name] = e
        log(f"\nTag {tag} complete")

    for failure in failures:
        error = failures[failure]
        log(f"Test {failure} failed with error:\n {error}")


class Testable:
    """
    Mixin for classes which allows them to be tested.
    To test just add a function decorated with @frontend_lib.mark_test
    Optionally providing a test_tag and test_name
    """

    def __init__(self):
        add_class_test(self)


# UI
def vspace():
    return v.Html(tag="br")


def hspace():
    return v.Html(tag="span", style_="padding: 0.5em")


def bold(text, **kwargs):
    return v.Html(tag="b", children=[text], **kwargs)


def italic(text, **kwargs):
    return v.Html(tag="i", children=[text], **kwargs)


def heading(text, level=1, **kwargs):
    return v.Html(tag=f"h{level}", children=[text], **kwargs)


def paragraph(*text, **kwargs):
    return v.Html(tag="p", children=text, **kwargs)


def image(src, alt="", width=200, **kwargs):
    return v.Img(src=src, alt=alt, width=width, **kwargs)


def centre(component, **kwargs):
    return v.Html(tag="center", children=[component], **kwargs)


def div(*children, **kwargs):
    return v.Html(tag="div", children=children, **kwargs)


def tabs(tab_headers, tab_items, **kwargs):
    tabs_ = [v.Tab(children=[tab]) for tab in tab_headers]
    tab_items_ = [v.TabItem(children=[tab_item]) for tab_item in tab_items]
    return v.Tabs(
        children=[
            *tabs_,
            *tab_items_,
        ],
        v_model=None,
        **kwargs
    )


def slider(minimum, maximum, int_only=False, **kwargs):
    if int_only:
        slider_ = widgets.IntSlider(height='40px', **kwargs)
        slider_.min = minimum
        slider_.max = maximum
        return slider_
    else:
        slider_ = widgets.FloatSlider(height='40px', **kwargs)
        slider_.min = minimum
        slider_.max = maximum
        return slider_


def help_dialog(page, children):
    """
    This creates a dialog box.
    To use put the output where you want the button to open the box appear.
    Provide as input the name of the page, and the content to be rendered in the box.
    """
    return v.Dialog(v_slots=[{
                        'name': 'activator',
                        'variable': 'x',
                        'children': v.Btn(
                            v_on='x.on',
                            color='success',
                            dark=True,
                            children=[
                                v.Icon(left=True, children=['mdi-help-circle']),
                                'Help'
                            ]),
                    }],
                    children=[
                        v.Card(children=[
                            v.CardTitle(children=[f'{page} help']),
                            v.CardText(children=[
                                children,
                                vspace(),
                            ]),
                        ]),
                    ])


def warning_dialog(children):
    return v.Dialog(width='500',
                 children=[
                     v.Card(children=[
                         v.CardTitle(children=["Warning"]),
                         v.CardText(children=[
                             children
                         ])
                     ])
                 ])
