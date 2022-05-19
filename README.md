# wordle-solver
AI Wordle solver that leverages unsupervised learning through outlier detection algorithms from the [PyOD library](https://link-url-here.org)

Final project for *CS 4701: Practicum in Artificial Intelligence* at Cornell University (Spring 2022)

Group members: Eric Gu, Jerilyn Zheng, Michelle Keoy

## Using the solver
The default algorithm used by the solver is Copula-Based Outlier Detection but this can be changed within _starting_word.py_. Run the solver using ```python wordle_solver.py```

Change parameters such as the desired dataset, number of iterations, and model type within _test.py_. Run the test suite using ```python test.py```
