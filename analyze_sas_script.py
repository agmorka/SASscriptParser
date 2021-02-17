
from SASscriptParser import *

path = r'H:\Documents\00_development\sprint23_STRY2219473_DoD_Default_files_WB\2.23.4.1.0-DoD_Default_files_WB_DSIP_integrity_tests.sas'
sas_parser = SASscriptParser(script_path=path)
sas_parser.parse()

def save_to_file(p: str, lst: list):
    with open(p, "w") as file:
        for item in lst:
            file.write(str(item))
            file.write('\n\n')

save_to_file(p=r"C:\Users\fu40av\!python\aaaa\comments.txt", lst=list(sas_parser.comments_list))
save_to_file(p=r"C:\Users\fu40av\!python\aaaa\macros.txt", lst=list(sas_parser.macros_list))
save_to_file(p=r"C:\Users\fu40av\!python\aaaa\statements.txt", lst=list(sas_parser.statements_list))
