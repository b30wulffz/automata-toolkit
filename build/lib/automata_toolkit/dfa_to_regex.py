from .regex_to_nfa import regex_to_nfa
from .nfa_to_dfa import nfa_to_dfa
from .dfa_to_efficient_dfa import dfa_to_efficient_dfa
from .visual_utils import draw_dfa
from .consts import Consts
import uuid

def union_regex(a, b):

    def split_into_unique(string):
        i=0
        j=0
        brac = 0
        result = []
        for c in string:
            if c == "(":
                brac+=1
            elif c == ")":
                brac-=1
            if brac == 0:
                if c == "+":
                    result.append(string[i:j])
                    i = j+1
            j+=1
        result.append(string[i:j])
        result = list(set(result))
        if "" in result:
            result.remove("")
        return result
    
    split_a = split_into_unique(a)
    split_b = split_into_unique(b)

    merged = list(set(split_a) | set(split_b))
    return "+".join(merged)

def concat_regex(a, b):
    if a=="" or b=="":
        return ""
    elif a[len(a)-1]==Consts.EPSILON:
        return "{}{}".format(a[:-1], b)
    elif b[0]==Consts.EPSILON:
        return "{}{}".format(a, b[2:])
    else:
        return "{}{}".format(a, b)

def cleene_star_regex(a):
    if a == Consts.EPSILON:
        return Consts.EPSILON
    elif a == "":
        return Consts.EPSILON
    else:
        return "{}*".format(bracket(a))

def bracket(a):
    # if a in [Consts.EPSILON, "", "a", "b"]:
    if len(a) <= 1:
        return a
    else:
        return "({})".format(a)

def dfa_to_regex(dfa):
    L = {}

    # find dead states
    is_not_dead = {}

    def is_final(state, visited):
        if state in dfa["final_reachable_states"]:
            return True
        else:
            visited.append(state)
            for alphabet in dfa["alphabets"]:
                next_state = dfa["transition_function"][state][alphabet]
                if next_state not in visited:
                    if is_final(next_state, visited) == True:
                        return True
        return False

    for state in dfa["reachable_states"]:
        is_not_dead[state] = is_final(state, [])

    # make new start state
    gnfa = {}
    gnfa["initial_state"] = uuid.uuid4()
    gnfa["final_states"] =  [uuid.uuid4()]
    gnfa["initial_state"] = "P0"
    gnfa["final_states"] =  ["P1"]

    gnfa["states"] = [gnfa["initial_state"]]
    gnfa["states"].extend(dfa["reachable_states"])
    gnfa["states"].extend(gnfa["final_states"])

    gnfa["alphabets"] = list(set(dfa["alphabets"]) | set([Consts.EPSILON]))


    gnfa["transition_function"]= {}
    # attach initial state of gnfa to initial state of dfa with epsilon transition
    gnfa["transition_function"][gnfa["initial_state"]] = {Consts.EPSILON: dfa["initial_state"]}

    # append rest of the transitions of dfa to gnfa
    for state in dfa["reachable_states"]:
        gnfa["transition_function"][state] = {}
        for alphabet in dfa["alphabets"]:
            next_state = dfa["transition_function"][state][alphabet]
            # appending only those which are not reachable from themselves from 
            if is_not_dead[next_state]:
                gnfa["transition_function"][state][alphabet] = next_state

    # attach final states of dfs to final state of gnfa with epsilon transition
    for state in dfa["final_reachable_states"]:
        gnfa["transition_function"][state][Consts.EPSILON] = gnfa["final_states"][0]

    gnfa["transition_function"][gnfa["final_states"][0]] = {}


    for state_1 in gnfa["states"]:
        L[state_1] = {}
        for state_2 in gnfa["states"]:
            L[state_1][state_2] = []
        for alphabet, next_state in gnfa["transition_function"][state_1].items():
            L[state_1][next_state].append(alphabet)
    visited = []

    reachable_non_dead_states = filter(lambda x: is_not_dead[x], dfa["reachable_states"])

    # removing states one by one gnfa["states"]:
    for chosen_state in reachable_non_dead_states:
        # for cleene star

        string = ""
        for transition_string in L[chosen_state][chosen_state]:
            string = union_regex(string, transition_string)
        if string != "":
            string = cleene_star_regex(string)
            L[chosen_state][chosen_state] = [string]

            # for appending star with next values
            next_states =  list(gnfa["transition_function"][chosen_state].items())
            for alphabet, next_state in next_states:
                del gnfa["transition_function"][chosen_state][alphabet]
                if chosen_state != next_state:
                    for ind in range(len(L[chosen_state][next_state])):
                        L[chosen_state][next_state][ind] = concat_regex(string, L[chosen_state][next_state][ind])
                        gnfa["transition_function"][chosen_state][L[chosen_state][next_state][ind]] = next_state
                    
        # concatenating prev state of chosen state to next states of chosen state
        for prev_state in gnfa["states"]:
            if prev_state != chosen_state:
                prev_next_states = list(gnfa["transition_function"][prev_state].items())
                
                for alphabet, next_state in prev_next_states:
                    if next_state == chosen_state:
                        # connecting prev_state to next of chosen
                        all_new_strings = []
                        for chosen_state_alphabet, chosen_next_state in gnfa["transition_function"][chosen_state].items():
                            new_strings = []
                            for prev_to_chosen in L[prev_state][chosen_state]:
                                chosen_to_next = chosen_state_alphabet
                                string = concat_regex(prev_to_chosen, chosen_to_next)
                                gnfa["transition_function"][prev_state][string] = chosen_next_state
                                new_strings.append(string)
                                all_new_strings.append(string)

                            L[prev_state][chosen_next_state].extend(new_strings)
                        if alphabet not in all_new_strings:
                            del gnfa["transition_function"][prev_state][alphabet]
    regex = ""
    for transition_string in L[gnfa["initial_state"]][gnfa["final_states"][0]]:
        regex = union_regex(regex, transition_string)
    regex = bracket(regex)
    return regex

if __name__=="__main__":
    # reg_exp = "a(a+b)*b"
    # reg_exp = "ab"
    # reg_exp = "(a+ab)(a+ab)*"
    reg_exp = "(a+b)*b"
    # reg_exp = "a+(a+b)*a"

    nfa = regex_to_nfa(reg_exp)
    dfa = nfa_to_dfa(nfa)
    new_dfa = dfa_to_efficient_dfa(dfa)
    draw_dfa(new_dfa, "[Minimized] {}".format(reg_exp))
    new_reg_exp = dfa_to_regex(new_dfa)
    print(new_reg_exp)
