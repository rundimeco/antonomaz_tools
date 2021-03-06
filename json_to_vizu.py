from antono_tools import *
import re


header = open_utf8("visualisation_tools/head.html")

dic_titres = get_json("data/dico_titres_ID.json")

out = ""
table_header = []
cpt = 0
for ID, infos in dic_titres.items():
#  if int(ID)>10:
#    break
  if len(table_header) == 0:
    table_header = infos.keys()
    out+="  <tr><th>ID</th><th>%s</th></tr>\n"%"</th><th>".join(table_header)
#  infos["Notice"] = re.escape(infos["Notice"])
  elems = [infos[cle] for cle in table_header]
  elems = [str(x) if str(x)!="null" and str(x)!="None" else "" for x in elems]
  this_info = "</td><td>".join(elems)
  l = f"  <tr><td>{ID}</td><td>{this_info}</td></tr>\n"
  out +=l
out_html = re.sub("{{content_table}}", out, header)
write_utf8("test.html", out_html, verbose = True)
