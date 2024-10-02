# MultiChoiceLib

MultiChoiceLib is a one-day project, meaning that it was literally written in a day. As you can imagine, it has not extensively been tested for bugs, and it does not work at all on machines which cannot run bash.

Usage:
```python
from multichoicelib import MultiChoice

query = MultiChoice("Pick one:", ["apples", "cherries"])
    .wAccentColor("\033[33m") # yellow
    .wQuestionPrefix("\033[4m") # underline, don't override
    .wAnswerPrefix("] ", True) # override params are optional and default to false
    .wSelectedPrefix(") ", True) # if false, will append instead
    .addOption("oranges")() # evaluate

print(query.index, query.value)
```

Result:

![GIF image of result](https://github.com/user-attachments/assets/824a3c3c-3f49-4f0d-89f6-991eee31702b)
> Warp terminal with Grafbase theme

