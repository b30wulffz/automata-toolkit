from regex_to_nfa import regex_to_nfa
import itertools
from collections import Counter
from graphviz import Digraph
import tempfile

def find_permutation(state_list, current_state):
    for state in state_list:
        if Counter(current_state) == Counter(state):
            return state
    return current_state

def get_epsilon_closure(nfa, dfa_states, state):
    closure_states = []
    state_stack = [state]
    while len(state_stack) > 0:
        current_state = state_stack.pop(0)
        closure_states.append(current_state)
        alphabet = "E"
        if nfa["transition_function"][current_state][alphabet] not in closure_states:
            state_stack.extend(nfa["transition_function"][current_state][alphabet])
    closure_states = tuple(set(closure_states))
    return find_permutation(dfa_states, closure_states)

def nfa_to_dfa(nfa):
    dfa = {}
    
    dfa["states"] = ["phi"]
    for r in range(1, len(nfa["states"])+1):
        dfa["states"].extend(itertools.combinations(nfa["states"], r))
    
    # calculate epsilon closure of all states of nfa
    epsilon_closure = {}
    for state in nfa["states"]:
        epsilon_closure[state] = get_epsilon_closure(nfa, dfa["states"], state)
    dfa["initial_state"] =  epsilon_closure[nfa["initial_state"]]
    
    dfa["final_states"] = []
    for state in dfa["states"]:
        if state != "phi":
            for nfa_state in state:
                if nfa_state in nfa["final_states"]:
                    dfa["final_states"].append(state)
                    break

    dfa["alphabets"] = ["a", "b"]

    dfa["transition_function"]= {}
    for state in dfa["states"]:
        dfa["transition_function"][state] = {}   
        for alphabet in dfa["alphabets"]:
            if state == "phi":
                dfa["transition_function"][state][alphabet] = state
            else:
                transition_states = []
                if len(state) == 1:
                    nfa_state = state[0]
                    next_nfa_states = nfa["transition_function"][nfa_state][alphabet]
                    for next_nfa_state in next_nfa_states:
                        transition_states.extend(epsilon_closure[next_nfa_state])
                else:
                    for nfa_state in state:
                        nfa_state = tuple([nfa_state])
                        if dfa["transition_function"][nfa_state][alphabet] != "phi":
                            transition_states.extend(dfa["transition_function"][nfa_state][alphabet])
                transition_states = tuple(set(transition_states))

                if len(transition_states) == 0:
                    dfa["transition_function"][state][alphabet] = "phi"
                else:
                    # find permutation of transition states in states
                    dfa["transition_function"][state][alphabet] = find_permutation(dfa["states"], transition_states)
    
    state_stack = [dfa["initial_state"]]
    dfa["reachable_states"] = []
    while len(state_stack) > 0:
        current_state = state_stack.pop(0)
        if current_state not in dfa["reachable_states"]:
            dfa["reachable_states"].append(current_state)
        for alphabet in dfa["alphabets"]:
            next_state = dfa["transition_function"][current_state][alphabet]
            if next_state not in dfa["reachable_states"]:
                state_stack.append(next_state)

    return dfa

def draw_dfa(dfa, title=""):
    state_name = {}
    i = 0
    for state in dfa["reachable_states"]:
        if state == "phi":
            state_name[state] = "\u03A6"
        else:
            state_name[state] = "q{}".format(i).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            i+=1

    g = Digraph()
    g.attr(rankdir='LR')

    if title == "":
        title = r'\n\nDFA'
    else:
        title = r'\n\nDFA : '+title
    g.attr(label=title, fontsize='30')

    # mark goal states
    g.attr('node', shape='doublecircle')
    for state in list(set(dfa["final_states"]) & set(dfa["reachable_states"])):
        g.node(state_name[state])

    # add an initial edge
    g.attr('node', shape='none')
    g.node("")
    
    g.attr('node', shape='circle')
    g.edge("", state_name[dfa["initial_state"]])

    for state in dfa["reachable_states"]:
        for character in dfa["transition_function"][state].keys():
            transition_state = dfa["transition_function"][state][character]
            g.edge(state_name[state], state_name[transition_state], label= character)

    g.view(tempfile.mktemp('.gv'))  


if __name__ == "__main__":
    reg_exp = "a(a+b)*b"
    nfa = regex_to_nfa(reg_exp)
    dfa = nfa_to_dfa(nfa)
    
    print()
    print(dfa["states"])
    print()
    print(dfa["initial_state"])
    print()
    print(dfa["final_states"])
    print()
    for state in dfa["transition_function"].keys():
        print(state,dfa["transition_function"][state])
    print()

    draw_dfa(dfa, reg_exp)