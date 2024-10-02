import pytest
from mkdocs_strings_replacement.config import _OldToNewStrings, StringsMarkdownReplacementPluginConfig

@pytest.mark.parametrize("replacements_list", [
    [
        {"old_value": "foo", "new_value": "bar"},
        {"old_value": "", "new_value": ""},
        {"old_value": "foo"*1000, "new_value": "bar"*1000}
    ],
    [
        {"old_value": "foo", "new_value": "bar"},
        {"old_value": "bar", "new_value": "test"}
    ],
    [
        {"old_value": "foo", "new_value": "bar"}
    ],
    [
        {"old_value": "", "new_value": ""}
    ],
    [
        {"old_value": "foo"*1000, "new_value": "bar"*1000}
    ]
])
def test_old_to_new_strings(replacements_list):
    for replacements in replacements_list:
        replacement = _OldToNewStrings()
        replacement.load_dict(replacements)
        errors, warnings = replacement.validate()
        assert not errors
        assert replacement.old_value == replacements['old_value']
        assert replacement.new_value == replacements['new_value']

@pytest.mark.parametrize("replacements", [
    [
        {"old_value": "foo", "new_value": "bar"}
    ],
    [
        {"old_value": "foo", "new_value": "bar"},
        {"old_value": "baz", "new_value": "qux"}
    ],
    [
        {"old_value": "hello", "new_value": "world"},
        {"old_value": "test", "new_value": "case"},
        {"old_value": "foo", "new_value": "bar"}
    ]
])
def test_strings_markdown_replacement_plugin_config(replacements):
    config = StringsMarkdownReplacementPluginConfig()
    config.load_dict({
        "strings_replacements": replacements
    })
    errors, warnings = config.validate()
    assert not errors
    assert len(config.strings_replacements) == len(replacements)
    for i, replacement in enumerate(config.strings_replacements):
        assert replacement.old_value == replacements[i]['old_value']
        assert replacement.new_value == replacements[i]['new_value']
        

# Parameterized test for invalid configurations
@pytest.mark.parametrize("config_data, expected_error", [
    ({"strings_replacements": "invalid"}, "expected a list of items"),
    ({"strings_replacements": [
        {"old_value": "foo", "new_value": 69}  # Invalid type, should be str
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420, "new_value": "bar"}  # Invalid type, should be str
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420, "new_value": 69}  # Invalid type, should be str
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420.123, "new_value": 69}  # Invalid type, should be str
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420.123, "new_value": 69.321}  # Invalid type, should be str
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420.123, "new_value": 69.321}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420.123, "new_value": 69.321},
        {"old_value": 11, "new_value": 32.33}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": "420.123", "new_value": "69.321"},
        {"old_value": 11, "new_value": 32.33}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": "420.123", "new_value": "69.321"},
        {"old_value": "11", "new_value": 32.33}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": "420.123", "new_value": "69.321"},
        {"old_value": 11, "new_value": "32.33"}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": "420.123", "new_value": 69.321},
        {"old_value": "11", "new_value": "32.33"}
    ]}, "expected type"),
    ({"strings_replacements": [
        {"old_value": 420.123, "new_value": "69.321"},
        {"old_value": "11", "new_value": "32.33"}
    ]}, "expected type"),
])
def test_strings_markdown_replacement_plugin_config_invalid(config_data, expected_error):
    config = StringsMarkdownReplacementPluginConfig()
    config.load_dict(config_data)
    errors, warnings = config.validate()
    assert any(expected_error in str(error).lower() for error in errors)