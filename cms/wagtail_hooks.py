from wagtail import hooks
from django.utils.html import format_html

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
