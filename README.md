# Searching For Knapsack

This repository contains a list of algorithms implemented by Python to solve Knapsack problem.

Link to report: [link-to-report](https://docs.google.com/document/d/1THMnSFJGdC9_s_IoWq08Qym4eB9wmkJr2G_1JIDEjrw/edit?usp=sharing)

Implementation of several algorithms for solving 1/0 knapsack problem on Python.

Here are implemented 5 algorithms:

## List of Algorithms:

- Brute force
- Branches and bounds
- Local beams
- Genetic algorithms

## Installation

To get started, follow the instructions below to install the necessary dependencies:

1. Make sure you have Python 3.x installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the project's root directory.
4. Run the following command to install `numpy`:

```bash
pip3 install numpy
```

## Data Generation

Before running any files in the `src/` directory, you need to generate the required data using the `generate-data.py` script. Follow the steps below:

1. Open a terminal or command prompt.
2. Navigate to the `script/` directory.
3. Run the following command to execute the `generate-data.py` script:
```bash
python3 generate-data.py
```
This script will generate the necessary data for subsequent file executions.

## Running the algorithm file

Once you have generated the data, you can run each algorithm located in the `src/` directory. Each file serves a specific algorithm according to its name. Follow the steps below to execute these files:

1. Open a terminal or command prompt.
2. Navigate to the `src/` directory.
3. Run the following command to execute each file:
```bash
python3 <file_name>.py
```

Replace `file_name.py` with the name of the specific file you want to run.
- Brute force: `knapsack-bruteforce.py`
- Branches and bounds: `knapsack-branch-bound.py`
- Local beams: `knapsack-local-beam.py`
- Genetic algorithms: `knapsack-genetic.py`


## Additional Notes

- Make sure to read the documentation provided within each file to understand its purpose and usage.
- Feel free to explore and modify the code to suit your needs.
- If you encounter any issues or have questions, please open an issue in this repository.

Happy coding!


