from pathlib import Path

from jinja2 import Environment, FileSystemLoader

template_dir = Path("/Users/parsashemirani/Main/htmltemps")


env = Environment(
    loader=FileSystemLoader(template_dir)
)


def generate_html(template_name, **kwargs):
    template = env.get_template(template_name)
    html = template.render(**kwargs)
    return html

"""
from app.tools.html_making import generate_html as gh
htman = gh('jamie1.html', title='timidtitle', username='masteruiser', message='hello you are a hydroflask waterbottle', items_count=4)
"""