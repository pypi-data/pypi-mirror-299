import re

def search(text: str, regex: str, ignore_whitespace=True) -> str | None:
	if ignore_whitespace:
		regex = ' '.join(regex.split()).replace(' ', '\s*')
	
	try:
		if pattern := re.search(regex.strip(), text):
			if match := pattern.groups():
				return match[0]
	except:
		return ""

