## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Part 1: Calculate Elevator Requirements](#part-1-calculate-elevator-requirements)
  - [Part 2: Simulate Elevator Scheduling](#part-2-simulate-elevator-scheduling)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Overview

This project provides a Python-based tool to:

1. Calculate elevator system requirements via the OpenAI API.
2. Simulate elevator scheduling in a building using simple assignment rules.

Whether you need rough estimates for elevator capacity or want to test scheduling logic, this script delivers clear results and is easy to extend.

---

## Prerequisites

Ensure you have:

* **Python**: Version 3.8 or higher
* **OpenAI API Key**
* **Git** (optional, for repository cloning)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/elevator-system.git
   cd elevator-system
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .\.venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root with:

   ```text
   OPEN_AI_API_KEY=your-real-api-key
   ```

---

## Usage

### Part 1: Calculate Elevator Requirements

1. Run the script:

   ```bash
   python elevator_system.py
   ```

2. Enter the requested values when prompted:

   * Number of floors
   * Maximum building capacity (total people)
   * Peak people per 5 minutes
   * Average travel time per floor (seconds)
   * Desired maximum wait time (seconds)

3. The output will be a single-line tuple:

   ```
   Tuple: (capacity, number_of_people, number_of_lifts)
   ```

   * `capacity` — Recommended people per elevator
   * `number_of_people` — Peak demand as entered
   * `number_of_lifts` — Calculated elevators needed

---

### Part 2: Simulate Elevator Scheduling

Use the `Building` class from a Python session:

```python
from elevator_system import Building

# Initialize a building with X floors, Y elevators, each with Z capacity
building = Building(floors=10, num_lifts=2, capacity=15)

# Add elevator calls
building.add_request(3, "up")
building.add_request(5, "down")
```

The console will print which elevator handles each request. Modify:

* **`assign_elevator`** logic for advanced assignment strategies
* **`is_full`** threshold to adjust load behavior

---

## Project Structure

```
├── elevator_system.py   # Main script: requirement calc + scheduling logic
├── requirements.txt     # Python packages
└── README.md            # Project documentation
```

---

## Contributing

Contributions are welcome! To submit changes:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:

   ```bash
   git commit -m "Describe your change"
   ```
4. Push the branch and open a pull request.

Feedback helps improve this tool—thanks for your input!
