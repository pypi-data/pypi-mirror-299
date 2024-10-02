import subprocess
import os

thisfolder = os.path.abspath(os.path.dirname(__file__)) + "/"
storagepath = thisfolder + "storage.txt"

class _Option:
    def __init__(self, options: list[str], index: int):
        self.value = options[index]
        self.index = index

class MultiChoice:
    _questionpfx = "\033[1m"
    _answerpfx = "⬦ "
    _selectedpfx = "⬥ "
    _accentcol = "\033[36m"

    def __init__(self, question, options=None):
        self.question = question
        self._options = [] # Prevent state retention error
        if options is not None:
            for opt in options:
                self.addOption(opt)

    def __call__(self) -> _Option:
        print(self._questionpfx, self.question, "\033[0m")
        return self._getInput()

    def addOption(self, option) -> "MultiChoice":
        self._options.append(option)
        return self

    def wQuestionPrefix(self, format, override=False) -> "MultiChoice":
        if override:
            self._questionpfx = format
        else:
            self._questionpfx += format
        return self

    def wAnswerPrefix(self, format, override=False) -> "MultiChoice":
        if override:
            self._answerpfx = format
        else:
            self._answerpfx += format
        return self

    def wSelectedPrefix(self, format, override=False) -> "MultiChoice":
        if override:
            self._selectedpfx = format
        else:
            self._selectedpfx += format
        return self

    def wAccentColor(self, col) -> "MultiChoice":
        self._accentcol = col
        return self

    def _buildCommandOpts(self):
        command = ["bash", thisfolder + "selection.sh"]
        command.append(storagepath)
        command.append(self._questionpfx)
        command.append(self._answerpfx)
        command.append(self._accentcol + self._selectedpfx)
        command += self._options
        return command

    def _getInput(self) -> _Option:
        subprocess.run(["chmod", "+x", thisfolder + "selection.sh"])
        subprocess.run(self._buildCommandOpts(), shell=False)
        with open(storagepath, "r") as file:
            selected = file.read().strip()
        os.remove(storagepath)
        return _Option(self._options, int(selected))