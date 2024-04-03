from __future__ import annotations as _annotations

from pathlib import Path
import re

import yaml
from jinja2 import Template  # type: ignore
from mkdocs.structure.pages import Page
from mkdocs.config import Config
from mkdocs.structure.files import Files

THIS_DIR = Path(__file__).parent
DOCS_DIR = THIS_DIR.parent
PROJECT_ROOT = DOCS_DIR.parent

def on_page_markdown(markdown: str, page: Page, config: Config, files: Files) -> str:
    """
    Called on each file after it is read and before it is converted to HTML.
    """

    if md := populate_people(markdown, page):
        return md
    else:
        return markdown

maintainers_template = Template(
"""
<div class="user-list user-list-center">
    {% for user in people.maintainers %}
    <div class="user">
        <a href="{{ user.url }}" target="_blank">
            <div class="avatar-wrapper">
                <img src="{{ user.avatarUrl }}"/>
            </div>
            <div class="title">@{{ user.login }}</div>
        </a>
    </div>
    {% endfor %}
</div>
"""
)


def populate_people(markdown: str, page: Page) -> str | None:
    if page.file.src_uri != 'people.md':
        return None

    # read people.yml file data
    with (THIS_DIR / 'people.yml').open('rb') as f:
        people = yaml.load(f, Loader=yaml.FullLoader)

    # Render the templates
    for name, template in [
        ('maintainers', maintainers_template),
    ]:
        rendered = template.render(people=people)
        markdown = re.sub(f'{{{{ {name} }}}}', rendered, markdown)

    return markdown
