# Rock Paper Scissor Lab

This project is an interactive hand-game duel using **Pygame**. It introduces students to dictionary-based rule lookups, automated CPU decision-making, temporary result display timers, and modular UI button interaction within an object-oriented codebase.
---

## What's Provided

A working Rock Paper Scissors game with:

- Three interactive choice buttons (`ROCK`, `PAPER`, `SCISSORS`) with mouse hover and click response states
- An automated computer opponent selecting moves at random
- Live scoreboard tracking player score and CPU score independently
- Timed result display that shows the outcome for 1.8 seconds before clearing picks for the next round

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left-click colored pads to repeat the sequence. Press R to restart after Game Over.


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the inverted outcome evaluation bug

Whenever the player plays a winning hand against the CPU, the game registers it as a loss. In game_engine.determine_winner(), the outcome lookup dictionary has inverted results for winning combinations: ("ROCK", "SCISSORS"), ("SCISSORS", "PAPER"), and ("PAPER", "ROCK") are assigned to "CPU" while losing combinations are assigned to "PLAYER". Correct the lookup table mappings so Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.

### Task 2: Implement "First to X Wins" match victory state

Currently, the game plays endlessly and keeps accumulating scores without a decisive match winner. Implement a target score ceiling . Once either the player or CPU reaches the target score, transition to a GAME_OVER match victory screen declaring the overall champion and prompt the player to press R to reset both scores.

### Task 3: Implement dynamic / adaptive AI counter-strategy

The CPU currently picks its move completely at random using random.choice(self.choices). Replace this with an adaptive AI strategy that tracks the player's choice history. If the player frequently favors one move (e.g., throwing Rock 60% of the time), bias the CPU's selection towards the counter-move to create an evolving challenge.

### Task 4: Implement hand gesture animated icons or icons reveal

The game displays picks only as simple plain text strings. Enhance game_engine.render() by drawing procedural geometric representations or icons for each move (a stone shape for Rock, a sheet outline for Paper, crossing blades for Scissors) with a brief shake animation before revealing both selections

---

## Expected Behavior

- Clicking any choice button selects that move, rolls a CPU choice, and evaluates the winner correctly.
- Rock beats Scissors, Scissors beats Paper, Paper beats Rock, and identical choices result in a Draw.
- Scores increment accurately and the round outcome stays visible for 1.8 seconds before clearing picks back to
---

## Folder Structure

```
rock_paper_scissors/
├── game/
│   ├── button.py
│   └── game_engine.py
├── main.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
