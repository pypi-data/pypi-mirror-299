import pytest
from unittest.mock import MagicMock
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs_strings_replacement.config import _OldToNewStrings, StringsMarkdownReplacementPluginConfig
from mkdocs_strings_replacement.plugin import StringsMarkdownReplacementPlugin

def convert_old_to_new_strings(replacements):
    instances = []
    for replacement in replacements:
        instance = _OldToNewStrings()
        instance.load_dict(replacement)
        instances.append(instance)
    return instances

@pytest.mark.parametrize("markdown, replacements, expected_output", [
    (
        "Hello world!", 
        [{"old_value": "world", "new_value": "universe"}], 
        "Hello universe!"
    ),
    (
        "Replace multiple values: foo, bar, baz.",
        [
            {"old_value": "foo", "new_value": "one"},
            {"old_value": "bar", "new_value": "two"},
            {"old_value": "baz", "new_value": "three"}
        ],
        "Replace multiple values: one, two, three."
    ),
    (
        "No replacements here.",
        [],
        "No replacements here."
    )
])
def test_on_page_markdown_valid_replacements(markdown, replacements, expected_output):
    plugin = StringsMarkdownReplacementPlugin()
    plugin.config = StringsMarkdownReplacementPluginConfig()
    plugin.config.load_dict({"strings_replacements": convert_old_to_new_strings(replacements)})

    config = MagicMock(spec=MkDocsConfig)
    result = plugin.on_page_markdown(markdown, config)
    
    assert result == expected_output

@pytest.mark.parametrize("replacements", [
    [{"old_value": "foo", "new_value": 123}],  # Invalid type, should be str
    "invalid",  # Not a list
])
def test_on_page_markdown_invalid_config(replacements):
    plugin = StringsMarkdownReplacementPlugin()
    plugin.config = StringsMarkdownReplacementPluginConfig()
    
    with pytest.raises(PluginError):
        plugin.config.load_dict({"strings_replacements": replacements})
        plugin.on_page_markdown("Sample markdown.", MagicMock(spec=MkDocsConfig))

def test_on_page_markdown_exception_handling():
    plugin = StringsMarkdownReplacementPlugin()
    plugin.config = StringsMarkdownReplacementPluginConfig()
    plugin.config.load_dict({"strings_replacements": convert_old_to_new_strings([{"old_value": "foo", "new_value": "bar"}])})

    config = MagicMock(spec=MkDocsConfig)

    with pytest.raises(PluginError):
        plugin.on_page_markdown(None, config)
