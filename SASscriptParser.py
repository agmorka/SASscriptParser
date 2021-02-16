import re


class SASscriptParser:
    """
        This class provides utility to parse SAS scripts (.sas files)
    """

    SAS_STATEMENT_PATTERNS = {
        'comment': r'/\*.*?\*/',
        'libname': r'(libname((?!;).*?);)',
        'data_step': r'(data ((?!run;).*?)run;)',
        'proc_step': r'(proc ((?!run;)(?!quit;).*?)(quit;|run;))',
        'filename': r'(filename((?!;).*?);)',
        'let_var': r'(\%let((?!;).*?);)',
        'put_var': r'(\%put((?!;).*?);)',
        'include': r'(\%include((?!;).*?);)',
        'options': r'(options((?!;).*?);)',
        'macro': r'((\%macro)(((?!\%macro)(?!\%mend).)*)(\%mend))',
        'call_macro': r'(\%((?!let )(?!put )[\w\d\s]+)(\(.*?\))?;)',
    }

    STATEMENT_TYPES_TO_EXTRACT = (
        'libname',
        'data_step',
        'proc_step',
        'filename',
        'let_var',
        'put_var',
        'include',
        'options',
        'call_macro',
    )

    def __init__(self, script_path: str):
        self.path = script_path
        self.__script_txt = ''
        self.comments_list = list()
        self.macros_list = list()
        self.statements_list = list()

    def _read_script(self):
        """
        This method reads .sas file
        To do: check whether provided file is a sas file.
        """
        try:
            with open(self.path) as file:
                self.__script_txt = file.read()
        except IOError:
            print(f'There is no such file: {self.path}')

    def _clean_script(self):
        """
        This method cleans SAS script:
        1. removes unnecessary marks (tabs, line breaks, multiple white-spaces, etc)
        2. lowers characters
        """
        to_remove_list = ('\n', '\t')
        for rm in to_remove_list:
            self.__script_txt = self.__script_txt.replace(rm, ' ')
        self.__script_txt = self.__script_txt.lower()
        self.__script_txt = ' '.join(self.__script_txt.split())

    def _remove_comments(self):
        """
        This method removes commented script fragments and appends removed comments to the list
        """
        sas_comment_pattern = re.compile(self.SAS_STATEMENT_PATTERNS['comment'])
        self.comments_list = re.findall(sas_comment_pattern, self.__script_txt)
        self.__script_txt = re.sub(sas_comment_pattern, '', self.__script_txt)

    def _extract_macros(self):
        """
        This method extracts SAS macro definitions from uploaded script and appends them to the list
        """
        sas_macro_pattern = re.compile(self.SAS_STATEMENT_PATTERNS['macro'])

        macro_searching_result = re.findall(sas_macro_pattern, self.__script_txt)
        while macro_searching_result:
            for macro in macro_searching_result:
                self.macros_list.append(macro[0])
                self.__script_txt = self.__script_txt.replace(macro[0], '')
            macro_searching_result = re.findall(sas_macro_pattern, self.__script_txt)

    def _disasamble_script(self):
        """
        This method separates SAS statements from the script and creates list of SAS statements
        """
        pattern = "(" + "|".join(
            [value for key, value in self.SAS_STATEMENT_PATTERNS.items() if key in self.STATEMENT_TYPES_TO_EXTRACT]) + ")"
        sas_statements_pattern = re.compile(pattern, flags=re.IGNORECASE)

        for statement in re.findall(sas_statements_pattern, self.__script_txt):
            for statement_type, pattern in self.SAS_STATEMENT_PATTERNS.items():
                if statement_type in self.STATEMENT_TYPES_TO_EXTRACT and re.search(pattern, statement[0]):
                    self.statements_list.append((statement_type, statement[0]))

    def parse(self):
        self._read_script()
        self._clean_script()
        self._remove_comments()
        self._extract_macros()
        self._disasamble_script()


if __name__ == "__main__":

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

