import json5
from PIL import ImageColor
import glob
import urllib.request

# https://stackoverflow.com/a/60978847
def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0].lower() + ''.join(i.capitalize() for i in s[1:])

def cleanup(text):
    return text.replace("/","").replace(","," ").replace("."," ")


urls = [
    "https://raw.githubusercontent.com/microsoft/vscode/refs/heads/main/extensions/theme-defaults/themes/light_vs.json",
    "https://raw.githubusercontent.com/microsoft/vscode/refs/heads/main/extensions/theme-defaults/themes/light_plus.json"
]
with open('vs-colors.tex', "w") as out:
    for url in urls:
        with urllib.request.urlopen(url) as f:
            theme = json5.load(f)
            if "colors" in theme.keys():
                for (k,v) in theme["colors"].items():
                    new_name = to_camel_case(cleanup(k))
                    rgb = ImageColor.getcolor(v,"RGB")
                    out.write(f"\\definecolor{{{new_name}}}{{RGB}}{{{','.join(tuple(map(str, rgb)))}}}%\"{v}\"\n")
            if "semanticTokenColors" in theme.keys():
                for (k,v) in theme["semanticTokenColors"].items():
                    new_name = cleanup(k)
                    rgb = ImageColor.getcolor(v,"RGB")
                    out.write(f"\\definecolor{{{new_name}}}{{RGB}}{{{','.join(tuple(map(str, rgb)))}}}%\"{v}\"\n")
            for x in theme['tokenColors']:
                if "name" in x.keys():
                    new_name = to_camel_case(cleanup(x['name']))
                elif isinstance(x['scope'],list):
                    new_name = to_camel_case(cleanup(x['scope'][-1]))
                else:
                    new_name = to_camel_case(cleanup(x['scope']))
                if not('foreground' in x['settings']):
                    continue
                oldcolor = x['settings']['foreground']
                rgb = ImageColor.getcolor(oldcolor,"RGB")
                out.write(f"\\definecolor{{{new_name}}}{{RGB}}{{{','.join(tuple(map(str, rgb)))}}}%\"{oldcolor}\"\n")
