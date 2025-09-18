from wagtail import hooks
from django.utils.html import format_html
from wagtail.admin.rich_text.editors.draftail.features import InlineStyleFeature
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

@hooks.register("insert_editor_js")
def editor_js():
    return format_html("""
        <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const categorySelect = document.querySelector('[name="category"]');
            const subcategorySelect = document.querySelector('[name="subcategory"]');
            if (!categorySelect || !subcategorySelect) return;

            const allOptions = Array.from(subcategorySelect.options);

            function filterSubcategories() {{
                subcategorySelect.innerHTML = '';
                allOptions.forEach(option => {{
                    if (!option.value) {{
                        subcategorySelect.appendChild(option);
                        return;
                    }}
                    if (option.text.includes(' - ')) {{
                        const [catName] = option.text.split(' - ');
                        if (catName === categorySelect.options[categorySelect.selectedIndex].text) {{
                            subcategorySelect.appendChild(option);
                        }}
                    }}
                }});
            }}

            filterSubcategories();
            categorySelect.addEventListener('change', filterSubcategories);
        }});
        </script>
    """)


@hooks.register("register_rich_text_features")
def register_highlight_feature(features):
    """
    Add a custom inline 'highlight' style to RichText editors, rendering as
    <span data-highlight="true">…</span> which we style to accent color + bold.
    """
    feature_name = "highlight"
    type_ = "HIGHLIGHT"

    control = {
        "type": type_,
        "label": "HL",
        "description": "Highlight (accent color)",
        # Optional: provide an icon via 'icon' key if desired
    }

    # Register the Draftail editor plugin
    features.register_editor_plugin(
        "draftail",
        feature_name,
        InlineStyleFeature(control),
    )

    # Define database <-> contentstate conversion rules
    db_conversion = {
        "from_database_format": {
            'span[data-highlight]': InlineStyleElementHandler(type_),
        },
        "to_database_format": {
            "style_map": {
                # Use element mapping dict instead of DOM helper to avoid NoneType errors
                type_: {"element": "span", "props": {"data-highlight": "true"}},
            },
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Make the feature available by default in all RichText editors
    if feature_name not in features.default_features:
        features.default_features.append(feature_name)
