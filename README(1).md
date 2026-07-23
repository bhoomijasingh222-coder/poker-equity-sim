# Poker Equity and Decision Simulator

A Python-based Texas Hold'em simulator that estimates showdown equity under incomplete information and evaluates call/fold decisions using pot odds and expected value.

The project combines Monte Carlo simulation, exact combinatorial enumeration, complete poker-hand evaluation, and automated testing. It supports incomplete or completed boards, multiple opponents, multiway ties, and validation of simulated equity against exact results when exhaustive calculation is computationally practical.

## Overview

Given:

- two player hole cards;
- zero to five community cards;
- a chosen number of opponents;
- a simulation count;
- the current pot; and
- the amount required to call,

the program reports:

- the player's strongest five-card hand when the board is complete;
- win, tie, and loss probabilities;
- estimated equity;
- the break-even equity required to call;
- expected profit from calling; and
- a simplified `CALL` or `FOLD` recommendation.

For completed heads-up boards, the program can also enumerate every legal opponent holding and compare the exact equity with the Monte Carlo estimate.

## Features

- Complete five-card hand classification and tie-breaking
- Best-five-of-seven Texas Hold'em hand evaluation
- Monte Carlo sampling without card replacement
- Support for one or more opponents
- Correct fractional equity for multiway ties
- Pot-odds and break-even equity calculation
- Expected-value-based call/fold analysis
- Exact heads-up enumeration on completed boards
- Absolute-error comparison between simulated and exact equity
- Input validation for cards, board size, opponents, and simulations
- Automated tests covering hand rankings, edge cases, exact results, and probability consistency

## Quantitative Methodology

### Monte Carlo equity

For every simulation, the program:

1. Removes the player's cards and known board cards from the deck.
2. Samples two legal cards for each opponent without replacement.
3. Samples any missing community cards.
4. Evaluates the best five-card hand available to every player.
5. Records whether the player wins, ties, or loses.
6. Assigns the player a fractional pot share in a tie.

Estimated equity is calculated as:

```text
equity = total player pot share / number of simulations
```

For example:

- a sole win contributes `1`;
- a two-player tie contributes `1/2`;
- a three-player tie contributes `1/3`; and
- a loss contributes `0`.

This makes equity different from win probability whenever ties are possible.

### Hand scoring

Each evaluated hand is represented by a tuple:

```text
(category, tie-break value 1, tie-break value 2, ...)
```

Categories are ordered from weakest to strongest:

| Score | Hand category |
|---:|---|
| 0 | High card |
| 1 | One pair |
| 2 | Two pair |
| 3 | Three of a kind |
| 4 | Straight |
| 5 | Flush |
| 6 | Full house |
| 7 | Four of a kind |
| 8 | Straight flush |

For example:

```text
(2, 14, 13, 7)
```

represents two pair, aces and kings, with a seven kicker. Python can compare these tuples lexicographically, allowing both hand categories and tie-break values to be compared consistently.

### Exact enumeration

When the board is complete and there is one opponent, seven cards are known:

```text
2 player cards + 5 board cards = 7 known cards
```

This leaves 45 cards in the deck. The number of possible two-card opponent holdings is:

```text
C(45, 2) = 990
```

The exact evaluator checks all 990 legal holdings. This provides a deterministic benchmark against which the Monte Carlo estimate can be validated.

Absolute estimation error is:

```text
absolute error = |Monte Carlo equity - exact equity|
```

### Pot odds and call EV

The required break-even equity is:

```text
required equity = call cost / (pot before call + call cost)
```

The expected profit from calling is:

```text
final pot = pot before call + call cost
expected return = estimated equity × final pot
call EV = expected return - call cost
```

The simplified decision rule is:

```text
call EV > 0  → CALL
call EV < 0  → FOLD
call EV = 0  → BREAK-EVEN
```

## Project Structure

```text
.
├── main.py
├── poker/
│   ├── __init__.py
│   ├── cards.py
│   ├── eval.py
│   ├── sim.py
│   ├── exact.py
│   └── decisions.py
└── tests/
    ├── test_cards.py
    ├── test_eval.py
    ├── test_sim.py
    ├── test_exact.py
    └── test_decisions.py
```

### Module responsibilities

- `cards.py`: card representation, parsing, validation, and deck creation
- `eval.py`: five-card scoring, best-five-of-seven evaluation, and readable hand descriptions
- `sim.py`: random dealing, multi-opponent simulation, and equity estimation
- `exact.py`: exact enumeration for completed heads-up boards
- `decisions.py`: required-equity and expected-value calculations
- `main.py`: command-line input, output, and orchestration
- `tests/`: automated correctness and consistency checks

## Requirements

- Python 3.10 or later recommended
- `pytest` for automated testing

The core simulator uses only the Python standard library.

## Installation

Clone the repository and enter its directory:

```bash
git clone <repository-url>
cd <repository-directory>
```

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the test dependency:

```bash
python -m pip install pytest
```

## Running the Simulator

From the project root, run:

```bash
python main.py
```

Cards use two-character notation:

- ranks: `2 3 4 5 6 7 8 9 T J Q K A`
- suits: `c d h s`

Examples:

```text
As = ace of spades
Qd = queen of diamonds
7h = seven of hearts
Tc = ten of clubs
```

Enter multiple cards separated by spaces:

```text
As Qs
Js 7s 2d
```

## Example

Input:

```text
Your two hand cards: Ah 7d
Board cards, or leave blank: As Kc Kd 4h 2s
Number of opponents: 1
Number of simulations: 20000
Current pot including the opponent's bet: 150
Amount required to call: 50
```

Representative output:

```text
Your best hand is: Two pair of Aces and Kings, with a Seven kicker
Hand score: (2, 14, 13, 7)

Win probability: 84.41%
Tie probability: 0.62%
Loss probability: 14.96%

Your estimated equity: 84.72%
Required equity: 25.00%
Expected profit from calling: 119.44

Decision: CALL

MONTE CARLO VALIDATION
Monte Carlo equity: 84.7225%
Exact equity: 84.5455%
Absolute error: 0.1770%
Exact opponent hands tested: 990
```

Monte Carlo results vary slightly between runs because the unknown cards are sampled randomly.

## Verified Exact Case

For:

```text
Player cards: Ah 7d
Board: As Kc Kd 4h 2s
Opponents: 1
```

exact enumeration produces:

| Outcome | Count | Probability |
|---|---:|---:|
| Wins | 834 | 84.2424% |
| Ties | 6 | 0.6061% |
| Losses | 150 | 15.1515% |
| Total | 990 | 100.0000% |

Heads-up ties contribute half of the pot, so exact equity is:

```text
(834 + 6 / 2) / 990 = 84.5455%
```

## Automated Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run a single test file:

```bash
python -m pytest tests/test_eval.py -v
```

The tests cover:

- creation and parsing of valid cards;
- rejection of invalid ranks and suits;
- construction of a 52-card deck without duplicates;
- every five-card hand category;
- ace-low straights;
- hand-category and kicker comparisons;
- selection of the best five cards from seven;
- guaranteed-win and guaranteed-tie simulations;
- exact enumeration totals and probabilities;
- decision calculations;
- outcome counts equalling the simulation count;
- win, tie, and loss probabilities summing to one; and
- equity remaining between zero and one.

## Assumptions

The current model assumes:

- opponent holdings are uniformly random among all legal cards;
- all unknown community cards are uniformly random;
- the entered pot already includes every opponent contribution made before the player's call;
- calling closes the action, so no further betting occurs;
- all players reach showdown after the call; and
- rake and transaction costs are ignored.

These assumptions make the output most appropriate for all-in decisions or simplified showdown analysis.

## Limitations

- Opponent betting ranges and playing tendencies are not modelled.
- The program does not estimate fold equity.
- Future betting decisions are not represented.
- Position, stack depth, bet sizing strategy, and table dynamics are excluded.
- Exact enumeration is currently limited to completed heads-up boards.
- Monte Carlo estimates contain sampling error.

The `CALL` or `FOLD` output is therefore a model-based recommendation rather than a complete poker strategy.

## Future Work

- Weighted opponent-range modelling
- Reproducible simulations using user-specified random seeds
- Confidence intervals for estimated equity
- Convergence and runtime analysis across simulation counts
- Performance profiling and caching
- Exact enumeration for additional computationally manageable states
- Continuous integration to run tests automatically
- Optional graphical or web interface

## Key Learning Outcomes

This project demonstrates:

- probabilistic modelling under incomplete information;
- Monte Carlo estimation;
- combinatorial enumeration;
- expected-value decision analysis;
- validation against deterministic benchmarks;
- careful treatment of ties and multi-agent outcomes;
- modular Python design; and
- automated software testing.

## Disclaimer

This project is intended for educational and analytical purposes. It does not guarantee profitable poker decisions and should not be treated as financial or gambling advice.

