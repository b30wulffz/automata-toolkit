# Automata Toolkit

Automata toolkit is a small library which contains tools to convert, minimize and visualize Regular Expressions, NFA and DFA.

## Installation

### Prerequisites

```bash
sudo apt install graphviz
pip install graphviz==0.16
```

### Install

```bash
pip install automata-toolkit
```

## Modules

### regex_to_postfix

- This module converts any given regular expression to its equivalent postfix expression.
- The conversion from regular expression to postfix representation makes use of Shunting Yard Algorithm which arranges the expression from left to right based on the priority order of operations.
- Functions are as follows:
  - regex_to_postfix(reg_exp)
  - is_alphabet(c)

### regex_to_nfa

- This module converts any given regular expression to its equivalent NFA.
- The conversion process is split into two parts: conversion of given expression to its postfix representation, and then using that postfix representation to create NFA.
- The conversion from regular expression to postfix representation makes use of Shunting Yard Algorithm which arranges the expression from left to right based on the priority order of operations.
- Then this postfix representation is converted to NFA using Thompson's construction algorithm, where characters from postfix representation are pushed into a queue, and operators are pushed into a stack. This stack is emptied and operations gets applied to the elements in the queue, once any opertor having lower or equal priority is about to get pushed into the stack.
- This is how it gives us an equivalent Non Deterministic Finite Automata.
- Functions are as follows:
  - regex_to_nfa(reg_exp)
  - get_alphabet_nfa(character, alphabets)
  - concat_nfa(nfa1, nfa2)
  - union_nfa(nfa1, nfa2)
  - cleene_star_nfa(nfa1)

### nfa_to_dfa

- This module converts a given NFA to its equivalent DFA.
- Initially the epsilon enclosure of all the states is calculated and stored in a dictionary.
- Then, DFA[start_state] = Epsilon[NFA[start_state]]
- Then for calculating the transitions, the program first calculates the Epsilon enclosure of that state, and then checks for alphabet based state transitions.
- And this is how we obtain a deterministic finite state automata. Note that DFA obtained may not be the minimal one.
- Functions are as follows:
  - nfa_to_dfa(nfa)
  - get_epsilon_closure(nfa, dfa_states, state)

### dfa_to_regex

- This module obtains a regular expression of the given DFA.
- Initially a GNFA is created by removing all the unreachable and dead states. Then we add a new start state with epsilon transition to original start stare, and connect all the original final states to a new final state using epsilon transitions.
- Now, all the states except the new initial, and final state, are removed one by one.
- While removing a particular state, the program first checks for any self loops. If multiple self loops exist, then program does a union of all these parallel transitions alphbets, and thus adds a cleene star over it.
- Then this cleen star value is concatenated to alphabets/strings of all the outgoing states.
- At the end, the incoming states'alphabets/strings are concatenated with the alphabets/strings of all the outgoing states, and then this state is removed.
- Upon iterating same procedure for all middle states, we arrive at a point when only initial and final states are left.
- The transition string between them is the required regular expression. Note that this regular expression might not be the simplified one.
- Functions are as follows:
  - dfa_to_regex(dfa)
  - union_regex(a, b)
  - concat_regex(a, b)
  - cleene_star_regex(a)
  - bracket(a)

### dfa_to_efficient_dfa

- This module calculates the minimal equivalent DFA for a given DFA.
- It makes use of Myhill Nerode theorem or in simple words, table filling algorithm.
- Initially a states\*states sized table is initialized with 0 value in all the cells.
- Then cell with final state, non-final state pairs are marked with 1.
- Then we check for unmarked state pairs, that whether any of their transition state pairs based on a particular alphabet value results in a marked cell.
- If yes, then mark that cell as 1, otherwise continue.
- This procedure is repeated multiple times until all the cell values achieve a stable state, i.e. they donot change.
- Now we merge all the unmarked state pairs. In order to merge this efficiently, this program uses union find data structure.
- After merging all the unmarked pairs, we obtain a minimal equivalent DFA.
- Functions are as follows:
  - dfa_to_efficient_dfa(dfa)

### visual_utils

- This module contains functions to visualize the NFA or DFA using `graphviz` library.
- Functions are as follows:
  - draw_nfa(nfa, title="")
  - draw_dfa(dfa, title="")

## Input Format

### Regular Expression

- string
- Input regular expression should be syntactically correct

### NFA

```
{
   "states": [
       <state_ids>,
       ...
   ],
   "initial_state": <initial_state_id>,
   "final_states": [
       <state_ids>,
       ...
   ],
   "alphabets": [
      "$",
       <alphabets>,
      ...
   ],
   "transition_function": {
       <state_id>: {
           <alphabet>: [
               <state_ids>,
           ],
           ... # transition for all alphabets shoud be present here
       },
       ...
   }
}
```

### DFA

```
{
   "states": [
       "phi",
       <state_ids>,
       ...
    ],
    "initial_state": <state_id>,
    "final_states":[
       <state_ids>,
       ...
    ],
    "alphabets": [
       <alphabets>,
       ...
    ],
    "transition_function": {
        <state_id>: {
            <alphabet>: <state_id>,
            ... # transition for all alphabets shoud be present here. In case of no transition, alphabet must point to phi
        },
        ...
    },
    "reachable_states": [
        <state_ids>,
        ...
    ],
    "final_reachable_states": [
        <state_ids>,
        ...
    ],
}
```

## Dependencies:

- Python 3
- Graphviz

> Note: Visualizer can generate visualizations but will not get triggered in WSL (Windows Subsystem for Linux). This library has been tested in Ubuntu, Elementary OS.

## Author

This project is developed by Shlok Pandey aka [b30wulffz](https://github.com/b30wulffz) and is licensed under the MIT License.
