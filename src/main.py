import click
import arrow
import requests
from jinja2 import Template
from operator import itemgetter
from pyquery import PyQuery as pq
from htmlmetadata import extract_metadata

BASE_TEMPLATE = Template("""
<link rel="stylesheet" href="/content/images/vertical-timeline.css"/>
<div id="myTimeline">
    {% for row in entries %}
    <div data-vtdate="{{ row.date_of }}">
        {{ row.html | safe }}
    </div>
    {% endfor %}
</div>
<script type="text/javascript" async defer src="/content/images/vertical-timeline.min.js"></script>
# <script type="text/javascript">
# jQuery( document ).ready(function() {
#     jQuery('#myTimeline').verticalTimeline({
#         startLeft: false,
#         alternate: true,
#         animate: "fade",
#         arrows: false
#     });
# });
# </script>
""")

@click.command()
@click.argument('url')
def cli(url):
    """
    Generate timeline html css script for vertical timeline.js
    http://ryanfitzgerald.github.io/vertical-timeline/
    """
    data = pq(url=url)
    entries = []
    entry_schema = {
        'html': None,
        'url': None,
        'date_of': None,
        'meta': None,
    }
    for card in  data('.kg-bookmark-card'):
        entry = entry_schema.copy()
        card_elem = pq(card)
        entry['html'] = card_elem.html()
        entry['url'] = card_elem.find('a.kg-bookmark-container').attr.href
        try:
            entry['meta'] = extract_metadata(entry['url'])
            entry['date_of'] = entry['meta'].get('summary', {}).get('date')

            # import pdb;pdb.set_trace()
        except Exception as e:
            print(f"could not extract meta from {entry['url']}, have to get date manually")
        if not entry['date_of']:
            # import pdb;pdb.set_trace()
            entry['date_of'] = click.prompt(click.style(f"Please enter a date for {entry['url']}", fg='green'), type=str)

        for fmt in ('DD MMMM YYYY', 'DD-MM-YYYY', 'MMMM YYYY', 'YYYY-MM-DD'):
            try:
                entry['date_of'] = arrow.get(entry['date_of'], fmt).format()
            except:
                continue

        entries.append(entry)

    print(BASE_TEMPLATE.render(entries=sorted(entries, key=itemgetter('date_of'), reverse=False)))
    # import pdb;pdb.set_trace()

if __name__ == '__main__':
    cli()