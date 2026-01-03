import pytest
import base64

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure the context to accept the maximized window size.
    'no_viewport': True is required when using '--start-maximized'.
    """
    return {
        **browser_context_args,
        "no_viewport": True
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Launch arguments for the browser to start maximized (Chromium only).
    """
    return {
        **browser_type_launch_args,
        "devtools": False,
        "args": ["--start-maximized"] + browser_type_launch_args.get("args", [])
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the Pytest HTML report to include a screenshot on failure.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # Add a sample link to the Links column (demonstration)
        extra.append(pytest_html.extras.url("http://google.com/", name="Google"))
        
        page = None
        # Try to get 'page' from the request fixture if available
        # This is robust for pytest-bdd where direct funcargs might not show step fixtures
        if "request" in item.funcargs:
            request = item.funcargs["request"]
            try:
                page = request.getfixturevalue("page")
            except Exception:
                # Page fixture might not be used or verified
                pass
        
        # Fallback: Check funcargs directly
        if not page:
            page = item.funcargs.get("page")
            
        if page:
            try:
                # Capture screenshot as base64
                screenshot_bytes = page.screenshot()
                base64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
                
                # Embed in HTML
                # Using a standard img tag
                html = (
                    f'<div><img src="data:image/png;base64,{base64_img}" '
                    f'alt="screenshot" style="width:600px;height:auto;border:1px solid #ccc;" '
                    f'onclick="window.open(this.src)" /></div>'
                )
                extra.append(pytest_html.extras.html(html))
            except Exception as e:
                extra.append(pytest_html.extras.text(f"Failed to capture screenshot: {e}"))
        
        report.extra = extra
