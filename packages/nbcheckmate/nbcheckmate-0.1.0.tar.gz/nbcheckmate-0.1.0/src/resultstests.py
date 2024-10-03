import dill as pickle
import os
import subprocess

class ResultsTests:
    def __init__(self, name, **kwargs):
        
        self.variables = {}
        self.functions = {}
        self.name = name
        self.file_path = os.path.join('tests', f'test_{self.name}.pkl')
        
        for key, value in kwargs.items():
            if callable(value):
                self.functions[key]=value
            else :
                self.variables[key]=value
                
    def _locate_tests(self):

        cwd = os.getcwd()

        # while not os.path.isdir(os.path.join(cwd, 'tests')):
        #     cwd = os.path.dirname(cwd)
        #     if cwd == os.sep:
        #         raise NameError(
        #             "Could not find /tests directory in any parent folder")

        tests_path = os.path.join(cwd, 'tests')
        
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
        