import asyncio
import json
import os
import traceback
import webbrowser
from contextlib import suppress
from pathlib import Path
from typing import Dict, Any

import pytest
from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse
from bantam.http import WebApplication


import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'example'))
from class_rest_get import RestAPIExampleAsync


PORT = 8082


class TestJavascriptGenerator:

    @pytest.mark.asyncio
    async def test_generate_basic(self):
        def assert_preprocessor(request: Request) -> Dict[str, Any]:
            assert isinstance(request, Request), "Failed to get valid response on pre-processing"
            return {}

        def assert_postprocessor(response: Response) -> None:
            assert isinstance(response, (StreamResponse, Response)), "Failed to get valid response for post-processing"

        RestAPIExampleAsync.result_queue = asyncio.Queue()
        root = Path(__file__).parent
        static_path = root.joinpath('static')
        app = WebApplication(static_path=static_path, js_bundle_name='generated', using_async=True)
        app.set_preprocessor(assert_preprocessor)
        app.set_postprocessor(assert_postprocessor)

        async def launch_browser():
            await asyncio.sleep(1.0)
            browser = None
            try:
                browser = webbrowser.get("chrome")
            except Exception:
                with suppress(Exception):
                    browser = webbrowser.get("google-chrome")
                if not browser:
                    browser = webbrowser.get()
            if not browser:
                os.write(sys.stderr.fileno(),
                         b"UNABLE TO GET BROWSER SUPPORT IN HEADLESS CONFIGURATION. DEFAULTING TO NON_HEADLESS")
                browser = webbrowser.get()
            browser.open(f"http://localhost:{PORT}/static/index_async.html")
            result = await RestAPIExampleAsync.result_queue.get()
            await asyncio.sleep(2.0)
            await app.shutdown()
            return result

        try:
            completed, _ = await asyncio.wait([app.start(modules=['class_rest_get'], port=PORT),
                                               launch_browser()], timeout=100000, return_when=asyncio.FIRST_COMPLETED)
            results = [c.result() for c in completed if c is not None]
        except Exception as e:
            assert False, f"Exception processing javascript results: {traceback.format_exc()}"
        if any([isinstance(r, Exception) for r in results]):
            assert False, "At least one javascript test failed. See browser window for details"
        assert results[0] == "PASSED", \
            "FAILED JAVASCRIPT TESTS FOUND: \n" + \
            "\n".join([f"{test}: {msg}" for test, msg in json.loads(results[0]).items()])
