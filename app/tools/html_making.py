from pathlib import Path
import os
from jinja2 import Environment, FileSystemLoader

templates_dir = Path("/Users/parsashemirani/Main/html/templates/")
rendered_dir = Path("/Users/parsashemirani/Main/html/rendered/")

env = Environment(
    loader=FileSystemLoader(templates_dir)
)


def generate_html(template_name, **kwargs):
    numbers = []
    for p in rendered_dir.iterdir():
        if p.suffix.lower() == ".html":
            if p.stem.isdigit():
                numbers.append(int(p.stem))
    new_num = (max(numbers) if numbers else 0) + 1

    template = env.get_template(template_name)
    html = template.render(**kwargs)
    output_path = rendered_dir / f"{new_num}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return new_num


"""
from app.tools.html_making import generate_html as gh
names_list = ['Tony', 'Gulasdfadfasdfar', 'Parsasdfasdfasda', 'Timiasadfasdfasd James', 'Masdfasdfadfasdfsdfaster man', 'Foo bar', 'Hydroflask']
result = gh(
    template_name='mastertemp.html',
    names=names_list,
    username='XxijingpingxX'
)
/Users/parsashemirani/Main/Inbox/thelevels/templates/stopwatches.html
"""

