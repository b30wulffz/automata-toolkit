from regex_to_postfix import regex_to_postfix, is_alphabet
import uuid
from graphviz import Digraph
import tempfile

def get_alphabet_nfa(character):
    nfa = {}
    nfa["states"] = [uuid.uuid4(), uuid.uuid4()]
    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = [nfa["states"][1]]
    nfa["alphabets"] = ["a", "b", "E"]
    nfa["transition_function"]= {}
    for state in nfa["states"]:
        nfa["transition_function"][state] = {}
        for alphabet in nfa["alphabets"]:
            nfa["transition_function"][state][alphabet] = []
    nfa["transition_function"][nfa["initial_state"]][character] = nfa["final_states"] 
    return nfa

def concat_nfa(nfa1, nfa2):
    nfa = {}

    nfa["states"] = []
    nfa["states"].extend(nfa1["states"])
    nfa["states"].extend(nfa2["states"])

    nfa["initial_state"] = nfa1["initial_state"]
    nfa["final_states"] = nfa2["final_states"]
    nfa["alphabets"] = ["a", "b", "E"]

    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        elif state in nfa2["states"]:
            nfa["transition_function"][state] = nfa2["transition_function"][state]

    # connect final states of nfa1 with start state of nfa2 using epsilon transition
    for state in nfa1["final_states"]:
        nfa["transition_function"][state]["E"].append(nfa2["initial_state"])

    return nfa

def union_nfa(nfa1, nfa2):
    nfa = {}

    nfa["states"] = [uuid.uuid4()]
    nfa["states"].extend(nfa1["states"])
    nfa["states"].extend(nfa2["states"])

    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = []
    nfa["final_states"].extend(nfa1["final_states"])
    nfa["final_states"].extend(nfa2["final_states"])
    nfa["alphabets"] = ["a", "b", "E"]

    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        elif state in nfa2["states"]:
            nfa["transition_function"][state] = nfa2["transition_function"][state]
        else:
            # nfa["transition_function"][state] = {"a": [], "b": [], "E": []}
            nfa["transition_function"][state] = {}
            for alphabet in nfa["alphabets"]:
                nfa["transition_function"][state][alphabet] = []
    
    # connecting start state to start state of nfa 1 and nfa 2 through epsilon move
    nfa["transition_function"][nfa["initial_state"]]["E"].extend([nfa1["initial_state"], nfa2["initial_state"]])
    return nfa

def cleene_star_nfa(nfa1):
    nfa = {}

    nfa["states"] = [uuid.uuid4()]
    nfa["states"].extend(nfa1["states"])
    nfa["states"].append(uuid.uuid4())

    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = [nfa["states"][  len(nfa["states"])-1 ]]
    nfa["alphabets"] = ["a", "b", "E"]
    
    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        else:
            # nfa["transition_function"][state] = {"a": [], "b": [], "E": []}
            nfa["transition_function"][state] = {}
            for alphabet in nfa["alphabets"]:
                nfa["transition_function"][state][alphabet] = []

    # connecting start state to start state of nfa 1 through epsilon move
    nfa["transition_function"][nfa["initial_state"]]["E"].append(nfa1["initial_state"])

    for final_state in nfa1["final_states"]:
        # connecting final states of nfa1 to start state of nfa1 through epsilon move
        nfa["transition_function"][final_state]["E"].append(nfa1["initial_state"])
        # connecting final states of nfa1 to final states of nfa through epsilon move
        nfa["transition_function"][final_state]["E"].extend(nfa["final_states"])

    # connecting start state to final state of nfa through epsilon move
    nfa["transition_function"][nfa["initial_state"]]["E"].extend(nfa["final_states"])
    return nfa
    
def regex_to_nfa(reg_exp):
    postfix_exp = regex_to_postfix(reg_exp)
    
    nfa_stack = []
    for character in postfix_exp:
        if is_alphabet(character):
            nfa_stack.append(get_alphabet_nfa(character))
        elif character == "?": # concat
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(concat_nfa(nfa1, nfa2))
        elif character == "+": # union
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(union_nfa(nfa1, nfa2))
        elif character == "*": # cleene star
            nfa1 = nfa_stack.pop()
            nfa_stack.append(cleene_star_nfa(nfa1))
    nfa = nfa_stack.pop()
    return nfa

def draw_nfa(nfa):
    g = Digraph()
    g.attr(rankdir='LR')
    g.attr('node', shape='doublecircle')
    for state in nfa['final_states']:
        g.node(str(state))
    g.attr('node', shape='circle')
    for state in nfa["states"]:
        for character in nfa["transition_function"][state]:
            for transition_state in nfa["transition_function"][state][character]:
                g.edge(str(state), str(transition_state), label= character)
    # mark goal states

    g.view(tempfile.mktemp('.gv'))  

if __name__ == "__main__":
    reg_exp = "a(a+b)*b"
    nfa = regex_to_nfa(reg_exp)
    print()
    print(nfa["states"])
    print()
    print(nfa["initial_state"])
    print()
    print(nfa["final_states"])
    print()
    for state in nfa["transition_function"].keys():
        print(state,nfa["transition_function"][state])
    print()
    draw_nfa(nfa)