"""Browser regressions; run with .venv/bin/python -m unittest discover -s tests."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

from playwright.sync_api import sync_playwright

spec = importlib.util.spec_from_file_location(
    "exporter", Path(__file__).resolve().parents[1] / "export-google-book.py"
)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ReaderNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.set_content('''
            <input aria-label="Page" value="46">
            <canvas width="400" height="500"></canvas>
            <script>
            const input = document.querySelector('input');
            const canvas = document.querySelector('canvas');
            const ctx = canvas.getContext('2d');
            function render(n) {
                ctx.fillStyle = n % 2 ? 'navy' : 'maroon';
                ctx.fillRect(0, 0, 400, 500);
            }
            render(46);
            </script>
        ''')
        self.timeout = patch.object(exporter, 'NAV_CHANGE_TIMEOUT', 2)
        self.settle = patch.object(exporter, 'RENDER_SETTLE_SECONDS', 0.3)
        self.timeout.start()
        self.settle.start()

    def tearDown(self):
        self.timeout.stop()
        self.settle.stop()
        self.page.close()

    def test_rejected_jump_is_not_success(self):
        self.page.evaluate('''() => input.onkeydown = e => {
            if (e.key === 'Enter') setTimeout(() => input.value = '46', 100);
        }''')
        self.assertFalse(exporter.jump_to_reader_page(self.page, 47, attempts=1))

    def test_page_one_is_actually_requested(self):
        self.page.evaluate('''() => input.onkeydown = e => {
            if (e.key === 'Enter') setTimeout(() => render(Number(input.value)), 100);
        }''')
        self.assertTrue(exporter.jump_to_reader_page(self.page, 1, attempts=1))
        self.assertEqual(exporter.read_reader_page_number(self.page), 1)

    def test_hidden_control_does_not_confirm_jump(self):
        self.page.evaluate('''() => input.onkeydown = e => {
            if (e.key === 'Enter') input.style.display = 'none';
        }''')
        self.assertFalse(exporter.jump_to_reader_page(self.page, 47, attempts=1))

    def test_counter_alone_does_not_confirm_next_page(self):
        _, digest, _, box = exporter.capture_page(self.page)
        visual = exporter.visible_page_digest(self.page, box)
        self.page.evaluate("input.value = '47'")
        changed, _ = exporter.wait_for_page_change_once(
            self.page, box, visual, digest, 46, timeout=1,
        )
        self.assertFalse(changed)

    def test_next_page_waits_for_delayed_render(self):
        _, digest, _, box = exporter.capture_page(self.page)
        self.page.evaluate('''() => {
            window.turns = 0;
            document.onkeydown = e => {
                if (e.key === 'ArrowRight') {
                    window.turns++;
                    input.value = '47';
                    setTimeout(() => render(47), 500);
                }
            };
        }''')
        self.assertTrue(exporter.advance_page(self.page, box, digest))
        self.assertEqual(self.page.evaluate('window.turns'), 1)
        self.assertNotEqual(exporter.capture_page(self.page)[1], digest)


if __name__ == '__main__':
    unittest.main()
