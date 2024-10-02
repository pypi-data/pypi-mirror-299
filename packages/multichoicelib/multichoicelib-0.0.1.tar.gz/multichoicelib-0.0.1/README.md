# MultiChoiceLib

MultiChoiceLib is a one-day project, meaning that it was literally written in a day. As you can imagine, it has not extensively been tested for bugs, and I am unsure whether it works at all on non unix-based machines due to half of it being written in bash.

Usage:
```python
query = MultiChoice("Pick one:", ["apples", "cherries"])
    .wAccentColor("\033[33m") # yellow
    .wQuestionPrefix("\033[4m") # underline, don't override
    .wAnswerPrefix("] ", True) # override params are optional and default to false
    .wSelectedPrefix(") ", True) # if false, will append instead
    .addOption("oranges")() # evaluate

print(query.index, query.value)
```

Result:

-# Warp terminal with Grafbase theme

