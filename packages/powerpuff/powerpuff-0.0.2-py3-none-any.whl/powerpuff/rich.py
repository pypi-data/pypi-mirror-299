from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.box import MINIMAL, SIMPLE
from pipe import map, filter, sort


@contextmanager
def table(*columns, show_header=False, show_footer=False):
	rows = []

	def append(*v):
		if any(v):
			rows.append(*v)

	yield append

	t = Table(box=SIMPLE)
	t.show_header = show_header
	t.show_footer = show_footer

	for c in columns:
		t.add_column(c)

	for r in rows | filter(all) | sort(key=lambda x: x[0]):
		t.add_row(*(r | map(str)))

	Console().print(t)

