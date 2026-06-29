import markdown

with open("description.md", "r") as f:
    md = f.read()

html = markdown.markdown(md)

with open("description.html", "w") as f:
    f.write(html)