## Shapley Value Calculator

### Overview

This Python package calculates Shapley values for cooperative game theory. Shapley values provide a fair way to distribute the total payoff among players in a cooperative game, based on their individual contributions.

### Installation

Using pip:

```bash
pip install shapley-value
```

### Usage

#### Basic Example

```python
from shapley_value import ShapleyCombinations

players = ['A', 'B', 'C']
coalition_values = {
    ('A',): 10,
    ('B',): 20,
    ('C',): 30,
    ('A', 'B'): 50,
    ('A', 'C'): 60,
    ('B', 'C'): 70,
    ('A', 'B', 'C'): 100
}

shapley_combinations = ShapleyCombinations(players)
shapley_values = shapley_combinations.calculate_shapley_values(coalition_values)
print(shapley_values)
```

### Features

- Calculates Shapley values for cooperative games
- Supports any number of players
- Handles coalition values as a dictionary
- Includes example usage

### Requirements

- Python 3.x
- `itertools` module

### License

MIT License

### Contributing

1. Fork the repository.
2. Make your changes.
3. Commit your changes.
4. Open a pull request.

### Authors

- newbie


### Version History

- 0.0.2: Initial release

