import dill as pickle
import os
from pathlib import Path
import subprocess

class ResultsTests:
    def __init__(self, name, **kwargs):
        
        self.variables = {}
        self.functions = {}
        self.name = name
        self.test_path = self._locate_tests()
        self.file_path = os.path.join(self.test_path, f'test_{self.name}.pkl')
        
        for key, value in kwargs.items():
            if callable(value):
                self.functions[key]=value
            else :
                self.variables[key]=value
                
    def _locate_tests(self):        
        # There is two possible locations for the tests directory
        # 1. In the same directory as the notebook
        # 2. In the parent directory of the notebook
        # We will check both locations
        
        cwd = Path.cwd()
        print(cwd)
        tests_path = Path(cwd, 'tests') if Path(cwd, 'tests').is_dir() else Path(cwd.parent, 'tests')
        if not tests_path.is_dir():
            raise NameError(
                "Could not find /tests directory in any parent folder")
        return tests_path

    def save(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_name):
        
        cwd = os.path.join(os.getcwd(), "src")

        while not os.path.isdir(os.path.join(cwd, 'tests')):
            cwd = os.path.dirname(cwd)
            if cwd == os.sep:
                raise NameError(
                    "Could not find /tests directory in any parent folder")

        file_path = os.path.join(cwd, 'tests', file_name)
        
        with open(file_path, 'rb') as f:
            return pickle.load(f)
        
    def get_results(self):
        file_path = f"test_{self.name}.py"
        command = ["python3", "-m", "pytest", "-v", "--color=yes", file_path]
        sub_process = subprocess.Popen(command,
                            cwd=os.path.join(os.getcwd(), 'tests'), # set current working directory
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        output, error = sub_process.communicate(b"")  # binary input passed as parameter
        result = output.decode("utf-8")

        if not "FAILED" in result:
            # tests_directory = 'tests'
            # if self.subdir:
            #     tests_directory = f'{tests_directory}/{self.subdir}'
            result = f"""
{result}\n
🔥 Congratulations, you've just completed the {self.name} step! 🔥\n
First, please verify that everything is correct :\n
\033[1;32mgit\033[39m status\n
Then, don't forget to save your progress :\n
\033[1;32mgit\033[39m add {self.file_path}\n
\033[32mgit\033[39m commit -m \033[33m'Completed {self.name} step'\033[39m\n
\033[32mgit\033[39m push origin main
"""

        return result
        