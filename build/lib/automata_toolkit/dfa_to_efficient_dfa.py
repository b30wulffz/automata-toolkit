from .regex_to_nfa import regex_to_nfa
from .nfa_to_dfa import nfa_to_dfa
from .visual_utils import draw_dfa

def dfa_to_efficient_dfa(dfa):
    table = {}
    new_table = {}
    for state in dfa["reachable_states"]:
        table[state] = {}
        new_table[state] = {}
        for again_state in dfa["reachable_states"]:
            table[state][again_state] = 0
            new_table[state][again_state] = 0
            
    # populate final, non final pairs
    for state in dfa["reachable_states"]:
        if state not in dfa["final_reachable_states"]:
            for again_state in dfa["final_reachable_states"]:
                table[state][again_state] = 1
                new_table[state][again_state] = 1
                table[again_state][state] = 1
                new_table[again_state][state] = 1

    while True:
        for state_1 in dfa["reachable_states"]:
            for state_2 in dfa["reachable_states"]:
                for alphabet in dfa["alphabets"]:
                    # transition for an alphabet
                    if new_table[state_1][state_2] == 0:
                        next_state_1 = dfa["transition_function"][state_1][alphabet]
                        next_state_2 = dfa["transition_function"][state_2][alphabet]
                        new_table[state_1][state_2] = table[next_state_1][next_state_2]
                        new_table[state_2][state_1] = table[next_state_1][next_state_2]
                    else:
                        break

        changed = False
        # check if something changed or not
        for state_1 in dfa["reachable_states"]:
            for state_2 in dfa["reachable_states"]:
                if new_table[state_1][state_2] == 1 and table[state_1][state_2] == 0:
                    table[state_1][state_2] = new_table[state_1][state_2]
                    changed = True
        if not changed:
            break
    
    # implementing union find to merge
    parent = {}
    for state in dfa["reachable_states"]:
        # parent[state] = state
        parent[state] = {"value": state, "states": [state]}

    def get_parent(current_state, all=False):
        parent_state = parent[current_state]
        while parent_state["value"] != current_state:
            current_state = parent_state["value"]
            parent_state = parent[current_state]
        if all:
            return parent_state
        else:
            return tuple(parent_state["states"])

    for state_1 in dfa["reachable_states"]:
        for state_2 in dfa["reachable_states"]:
            if state_1 != state_2 and table[state_1][state_2] == 0:
                # merge state 1 and 2
                parent_state_1 = get_parent(state_1, all=True)
                parent_state_2 = get_parent(state_2, all=True)
                parent[parent_state_2["value"]]["value"] = parent_state_1["value"]
                parent[parent_state_1["value"]]["states"] = list(set(parent_state_1["states"]) | set(parent_state_2["states"]))

    # now we can create our new dfa
    new_dfa = {}
    new_dfa["states"] = list(set([get_parent(state) for state in dfa["reachable_states"]]))
    new_dfa["initial_state"] = get_parent(dfa["initial_state"])
    new_dfa["final_states"] = list(set([get_parent(state) for state in dfa["final_reachable_states"]]))
    # new_dfa["alphabets"] = ["a", "b"]
    new_dfa["alphabets"] = dfa["alphabets"]

    new_dfa["transition_function"]= {}
    for state in new_dfa["states"]:
        new_dfa["transition_function"][state] = {}
        for alphabet in new_dfa["alphabets"]:
            new_dfa["transition_function"][state][alphabet] = get_parent(dfa["transition_function"][state[0]][alphabet])

    # extras
    new_dfa["reachable_states"]  = new_dfa["states"]
    new_dfa["final_reachable_states"]  = new_dfa["final_states"]
    return new_dfa

if __name__=="__main__":
    reg_exp = "a(a+b)*b"
    reg_exp = "ab*+a"

    nfa = regex_to_nfa(reg_exp)
    dfa = nfa_to_dfa(nfa)
    draw_dfa(dfa, reg_exp)
    new_dfa = dfa_to_efficient_dfa(dfa)
    draw_dfa(new_dfa, "[Minimized] {}".format(reg_exp))
       
    print()
    print(new_dfa["states"])
    print()
    print(new_dfa["initial_state"])
    print()
    print(new_dfa["final_states"])
    print()
    for state in new_dfa["transition_function"].keys():
        print(state,new_dfa["transition_function"][state])
    print()