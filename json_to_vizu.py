from antono_tools import *
import re


header = open_utf8("visualisation_tools/head.html")

dic_titres = get_json("data/dico_titres_ID.json")

out = "<table class = 'styled-table'>\n"
table_header = []
for ID, infos in dic_titres.items():
  if len(table_header) == 0:
    table_header = infos.keys()
    out+="  <tr><th>ID</th><th>%s</th></tr>\n"%"</th><th>".join(table_header)
#  infos["Notice"] = re.escape(infos["Notice"])
  elems = [infos[cle] for cle in table_header]
  elems = [str(x) if str(x)!="null" and str(x)!="None" else "" for x in elems]
  this_info = "</td><td>".join(elems)
  l = f"  <tr><td>{ID}</td><td>{this_info}%s</td></tr>\n"
  out +=l
out+="</table>"

out_html = re.sub("{{content}}", out, header)
write_utf8("test.html", out_html, verbose = True)
