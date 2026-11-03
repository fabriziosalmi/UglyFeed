"""Request-shape tests for the LLM provider clients.

Each test points a client at a local mock HTTP server and asserts the exact
request path, headers and JSON body that reach the wire. No real API is
called and no key is needed.
"""

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import llm_processor  # noqa: E402  pylint: disable=wrong-import-position

SYSTEM_PROMPT = ("You are a professional assistant, skilled in composing detailed "
                 "and accurate news articles from multiple sources.")

OPENAI_REPLY = {
    "id": "chatcmpl-test",
    "object": "chat.completion",
    "created": 0,
    "model": "gpt-test",
    "choices": [{
        "index": 0,
        "message": {"role": "assistant", "content": "openai ok"},
        "finish_reason": "stop",
    }],
    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
}

ANTHROPIC_REPLY = {
    "id": "msg_test",
    "type": "message",
    "role": "assistant",
    "model": "claude-test",
    "content": [{"type": "text", "text": "anthropic ok"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 1, "output_tokens": 1},
}


class _Recorder(BaseHTTPRequestHandler):
    """Records every POST and answers with a canned provider reply."""

    def do_POST(self):  # pylint: disable=invalid-name
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        url = urlsplit(self.path)
        self.server.requests.append({
            "path": url.path,
            "query": parse_qs(url.query),
            "headers": {k.lower(): v for k, v in self.headers.items()},
            "body": json.loads(raw) if raw else None,
        })
        reply = ANTHROPIC_REPLY if url.path.endswith("/messages") else OPENAI_REPLY
        payload = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):  # pylint: disable=redefined-builtin
        pass


class MockServerTestCase(unittest.TestCase):
    """Starts a fresh mock server per test."""

    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _Recorder)
        self.server.requests = []
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def only_request(self):
        self.assertEqual(len(self.server.requests), 1, self.server.requests)
        return self.server.requests[0]


class OpenAIRequestTest(MockServerTestCase):

    def _call(self, api_url, provider="openai"):
        client = llm_processor.APIClientFactory.create_client(provider, "test-key", api_url)
        return client.call_api("hello", "gpt-test")

    def assert_openai_request(self, req):
        self.assertEqual(req["path"], "/v1/chat/completions")
        self.assertEqual(req["query"], {})
        self.assertEqual(req["headers"]["authorization"], "Bearer test-key")
        self.assertEqual(req["body"]["model"], "gpt-test")
        self.assertEqual(req["body"]["messages"], [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "hello"},
        ])
        self.assertEqual(req["body"]["max_tokens"], 4096)
        self.assertEqual(req["body"]["temperature"], 0.7)

    def test_base_url(self):
        self.assertEqual(self._call(f"{self.base}/v1"), "openai ok")
        self.assert_openai_request(self.only_request())

    def test_base_url_trailing_slash(self):
        self.assertEqual(self._call(f"{self.base}/v1/"), "openai ok")
        self.assert_openai_request(self.only_request())

    def test_legacy_full_endpoint_url_is_normalized(self):
        # Configs written before the fix carry the full endpoint URL.
        self.assertEqual(self._call(f"{self.base}/v1/chat/completions"), "openai ok")
        self.assert_openai_request(self.only_request())

    def test_groq_legacy_full_endpoint_url_is_normalized(self):
        self.assertEqual(self._call(f"{self.base}/v1/chat/completions/", "groq"), "openai ok")
        self.assert_openai_request(self.only_request())


class OpenAIDefaultURLTest(unittest.TestCase):

    def test_default_urls_resolve_to_base_urls(self):
        for provider, expected in [
            ("openai", "https://api.openai.com/v1"),
            ("groq", "https://api.groq.com/openai/v1"),
            ("together", "https://api.together.xyz/v1"),
            ("mistral", "https://api.mistral.ai/v1"),
        ]:
            client = llm_processor.APIClientFactory.create_client(provider, "k")
            self.assertEqual(client.api_url, expected, provider)


class AzureRequestTest(MockServerTestCase):
    """Azure OpenAI: deployment in the path, api-version query, api-key header."""

    def _call(self, api_url, model="my-deployment", api_version=None):
        client = llm_processor.APIClientFactory.create_client(
            "azure", "test-key", api_url, api_version=api_version)
        return client.call_api("hello", model)

    def assert_azure_request(self, req, deployment="my-deployment",
                             api_version=llm_processor.AZURE_DEFAULT_API_VERSION):
        self.assertEqual(req["path"],
                         f"/openai/deployments/{deployment}/chat/completions")
        self.assertEqual(req["query"], {"api-version": [api_version]})
        self.assertEqual(req["headers"]["api-key"], "test-key")
        self.assertNotIn("authorization", req["headers"])
        self.assertEqual(req["body"]["messages"], [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "hello"},
        ])
        self.assertEqual(req["body"]["max_tokens"], 4096)

    def test_endpoint_and_deployment(self):
        self.assertEqual(self._call(self.base), "openai ok")
        self.assert_azure_request(self.only_request())

    def test_configured_api_version(self):
        self.assertEqual(self._call(f"{self.base}/", api_version="2025-04-01-preview"),
                         "openai ok")
        self.assert_azure_request(self.only_request(), api_version="2025-04-01-preview")

    def test_full_deployment_url_is_split(self):
        # An older config may hold the whole deployment URL.
        url = (f"{self.base}/openai/deployments/url-deployment/chat/completions"
               "?api-version=2024-06-01")
        self.assertEqual(self._call(url, model="gpt-4o"), "openai ok")
        self.assert_azure_request(self.only_request(), deployment="url-deployment",
                                  api_version="2024-06-01")

    def test_config_mapping(self):
        mapped = llm_processor.map_api_config({
            "selected_api": "Azure",
            "azure_endpoint": "https://res.openai.azure.com",
            "azure_api_key": "k",
            "azure_deployment": "dep",
            "azure_api_version": "2024-10-21",
        })
        self.assertEqual(mapped, {
            "provider": "azure",
            "api_key": "k",
            "model": "dep",
            "api_url": "https://res.openai.azure.com",
            "api_version": "2024-10-21",
        })
        llm_processor.validate_config(mapped)

    def test_missing_endpoint_is_a_config_error(self):
        with self.assertRaises(ValueError):
            llm_processor.validate_config(
                {"provider": "azure", "api_key": "k", "model": "dep"})


class AnthropicRequestTest(MockServerTestCase):

    def _client(self, **kwargs):
        return llm_processor.APIClientFactory.create_client(
            "anthropic", "test-key", f"{self.base}/v1/messages", **kwargs)

    def test_request_shape(self):
        result = self._client().call_api("hello", "claude-haiku-4-5-20251001")
        self.assertEqual(result, "anthropic ok")
        req = self.only_request()
        self.assertEqual(req["path"], "/v1/messages")
        self.assertEqual(req["headers"]["x-api-key"], "test-key")
        self.assertEqual(req["headers"]["anthropic-version"], "2023-06-01")
        self.assertEqual(req["headers"]["content-type"], "application/json")
        self.assertNotIn("authorization", req["headers"])
        self.assertEqual(req["body"], {
            "model": "claude-haiku-4-5-20251001",
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": "hello"}],
            "max_tokens": 4096,
        })

    def test_no_system_role_in_messages(self):
        self._client().call_api("hello", "claude-haiku-4-5-20251001")
        roles = [m["role"] for m in self.only_request()["body"]["messages"]]
        self.assertNotIn("system", roles)

    def test_temperature_sent_only_when_configured(self):
        self._client(temperature=0.2).call_api("hello", "claude-haiku-4-5-20251001")
        self.assertEqual(self.only_request()["body"]["temperature"], 0.2)

    def test_temperature_from_config_mapping(self):
        mapped = llm_processor.map_api_config({
            "selected_api": "Anthropic",
            "anthropic_api_key": "k",
            "anthropic_model": "claude-haiku-4-5-20251001",
            "anthropic_api_url": "https://api.anthropic.com/v1/messages",
            "anthropic_temperature": 0.3,
        })
        self.assertEqual(mapped["temperature"], 0.3)
        mapped = llm_processor.map_api_config({
            "selected_api": "Anthropic",
            "anthropic_api_key": "k",
            "anthropic_model": "claude-haiku-4-5-20251001",
        })
        self.assertIsNone(mapped.get("temperature"))


if __name__ == "__main__":
    unittest.main()
