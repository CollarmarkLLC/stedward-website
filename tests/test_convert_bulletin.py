import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts/convert_bulletin.py"
SPEC = importlib.util.spec_from_file_location("convert_bulletin", MODULE_PATH)
converter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(converter)


class ConvertBulletinTests(unittest.TestCase):
    def test_extracts_reorders_and_normalizes_sections(self):
        source = r"""Masthead

## **Holy Mass – Schedule & Intentions**
Sat  5:30p  For a special intention

## **Upcoming Events**
* Event one

## **Thoughts from Fr. Ryan**
The article.

## **For Your Information**
**NOTICE** Text\!

## **Assistants at Holy Mass**
| Date | Lector |
| --- | --- |

## **Our Return to the Lord**
| Budget | $ 1 |

## **Community Celebrations**
Happy Birthday

## **In Our Prayers Daily**
Please pray.

[image1]: <data:image/png;base64,AAAA>
"""
        sections, warnings = converter.extract_sections(source)
        result = converter.render("2026-08-16", "Twentieth Sunday", "green", sections)
        self.assertLess(result.index("## Thoughts"), result.index("## Upcoming"))
        self.assertIn("- Sat 5:30p For a special intention", result)
        self.assertIn("**NOTICE** Text!", result)
        self.assertNotIn("data:image", result)
        self.assertEqual([], warnings)

    def test_reports_missing_sections(self):
        sections, warnings = converter.extract_sections("## Thoughts from Fr. Ryan\nText")
        self.assertEqual("Text", sections["Thoughts from Fr. Ryan"])
        self.assertIn("missing section: Upcoming Events", warnings)

    def test_reads_title_and_color_from_normalized_liturgical_calendar(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            year = root / "2026"
            year.mkdir()
            (year / "liturgical-core.json").write_text(json.dumps({
                "days": [{
                    "date": "2026-08-23",
                    "liturgical": {"modern": {"selected": {
                        "title": "21st Sunday of Ordinary Time", "colors": ["green"],
                    }}},
                }],
            }), encoding="utf-8")
            self.assertEqual(
                converter.liturgical_calendar_metadata(root, "2026-08-23"),
                ("21st Sunday of Ordinary Time", "green"),
            )


if __name__ == "__main__":
    unittest.main()
