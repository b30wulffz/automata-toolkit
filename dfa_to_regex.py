from regex_to_nfa import regex_to_nfa
from nfa_to_dfa import nfa_to_dfa, draw_dfa
from dfa_to_efficient_dfa import dfa_to_efficient_dfa
import uuid
import time


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
    
    # def combine(string):
    #     return 

    split_a = split_into_unique(a)
    split_b = split_into_unique(b)

    merged = list(set(split_a) | set(split_b))
    return "+".join(merged)

    # if a=="":
    #     return b
    # elif b == "":
    #     return a
    # if a=="E" and b=="E":
    #     return "E"
    # else:   
    #     return "{}+{}".format(a,b)

def concat_regex(a, b):
    if a=="" or b=="":
        return ""
    elif a[len(a)-1]=="E":
        return "{}{}".format(a[:-1], b)
    elif b[0]=="E":
        return "{}{}".format(a, b[2:])
    else:
        return "{}{}".format(a, b)

def cleene_star_regex(a):
    if a == "E":
        return "E"
    elif a == "":
        return "E"
    else:
        # print("-> ", a)
        return "{}*".format(bracket(a))

def bracket(a):
    if a in ["E", "", "a", "b"]:
        return a
    else:
        return "({})".format(a)

def dfa_to_regex(dfa):
    L = {}

    # make new start state
    gnfa = {}
    gnfa["initial_state"] = uuid.uuid4()
    gnfa["final_states"] =  [uuid.uuid4()]

    gnfa["states"] = [gnfa["initial_state"]]
    gnfa["states"].extend(dfa["reachable_states"])
    gnfa["states"].extend(gnfa["final_states"])

    gnfa["alphabets"] = ["a", "b", "E"]

    gnfa["transition_function"]= {}
    # attach initial state of gnfa to initial state of dfa with epsilon transition
    gnfa["transition_function"][gnfa["initial_state"]] = {"E": dfa["initial_state"]}

    # append rest of the transitions of dfa to gnfa
    for state in dfa["reachable_states"]:
        gnfa["transition_function"][state] = dfa["transition_function"][state]

    # attach final states of dfs to final state of gnfa with epsilon transition
    for state in dfa["final_reachable_states"]:
        gnfa["transition_function"][state]["E"] = gnfa["final_states"][0]

    gnfa["transition_function"][gnfa["final_states"][0]] = {}

    # print(gnfa["initial_state"])
    # print(gnfa["final_states"])
    # print()

    for state_1 in gnfa["states"]:

        # alphabets = dfa["alphabets"]
        # if state_1 in dfa["final_reachable_states"]:
        #     alphabets = gnfa["alphabets"]

        L[state_1] = {}
        for state_2 in gnfa["states"]:
            if state_1 == state_2:
                L[state_1][state_2] = "E"
            else:
                L[state_1][state_2] = "" # "phi"
            for alphabet in gnfa["alphabets"]:
                if alphabet in gnfa["transition_function"][state_1].keys():
                    if state_2 == gnfa["transition_function"][state_1][alphabet]:
                        L[state_1][state_2] = union_regex(L[state_1][state_2], alphabet)

    # print(len(dfa["reachable_states"]))
    # print(len(gnfa["states"]))
    # initial_state = gnfa["initial_state"]
    # final_state = gnfa["final_states"][0]
    # print(initial_state)
    # print(L[initial_state][initial_state])

    # i = 1
    for state in dfa["reachable_states"]:
        for state_1 in gnfa["states"]:
            for state_2 in gnfa["states"]:
                L[state_1][state_1] = union_regex(L[state_1][state_1], concat_regex(L[state_1][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_1])))
                L[state_2][state_2] = union_regex(L[state_2][state_2], concat_regex(L[state_2][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_2])))
                L[state_1][state_2] = union_regex(L[state_1][state_2], concat_regex(L[state_1][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_2])))
                L[state_2][state_1] = union_regex(L[state_2][state_1], concat_regex(L[state_2][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_1])))
                # # print(state_1,state_2)
                # print()
                # print(L)
                # print()
                # time.sleep(5)
                # print(i)
                # i+=1

    initial_state = gnfa["initial_state"]
    final_state = gnfa["final_states"][0]
    new_reg_exp = concat_regex(cleene_star_regex(L[initial_state][initial_state]), concat_regex(L[initial_state][final_state], cleene_star_regex( union_regex( concat_regex(L[final_state][initial_state], concat_regex(cleene_star_regex(L[initial_state][initial_state]), L[initial_state][final_state])) , L[final_state][final_state]) )))
    return new_reg_exp


def dfa_to_regex_2(dfa):
    L = {}

    # find dead states
    # visited = []
    is_dead = {}
    is_not_dead = {}

    def is_final(state, visited):
        # if state in is_dead.keys():
        #     return not is_dead[state]
        # print("current ->", state_name_1[state])
        if state in dfa["final_reachable_states"]:
            # print(state_name_1[state], " final reachable")
            return True
        else:
            visited.append(state)
            res_a = False
            res_b = False
            next_state_a = dfa["transition_function"][state]["a"]
            if next_state_a not in visited:
                res_a = is_final(next_state_a, visited)
            
            next_state_b = dfa["transition_function"][state]["b"]
            if next_state_b not in visited:
                res_b = is_final(next_state_b, visited)
            # print(state_name_1[state], "->left ",state_name_1[next_state_a],res_a,"->right ",state_name_1[next_state_b],res_b )
            # print("->",state_name_1[next_state_a],res_a,"->",state_name_1[next_state_b],res_b )
            # print(res_a | res_b)
            if res_a == True or res_b == True:
                return True
        # print(state_name_1[state], " not final")
        return False

    #debug##########################################
    state_name_1 = {}
    i = 0
    for state in dfa["reachable_states"]:
        if state == "phi":
            state_name_1[state] = "\u03A6"
        else:
            state_name_1[state] = "q{}".format(i).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            i+=1
    ################################################            

    for state in dfa["reachable_states"]:
        # tmp_state = state
        # is_dead[state] = not is_final(state)
        is_not_dead[state] = is_final(state, [])
        print(state_name_1[state], is_not_dead[state])


    # make new start state
    gnfa = {}
    gnfa["initial_state"] = uuid.uuid4()
    gnfa["final_states"] =  [uuid.uuid4()]

    gnfa["states"] = [gnfa["initial_state"]]
    gnfa["states"].extend(dfa["reachable_states"])
    gnfa["states"].extend(gnfa["final_states"])

    gnfa["alphabets"] = ["a", "b", "E"]

    gnfa["transition_function"]= {}
    # attach initial state of gnfa to initial state of dfa with epsilon transition
    gnfa["transition_function"][gnfa["initial_state"]] = {"E": dfa["initial_state"]}

    # append rest of the transitions of dfa to gnfa
    for state in dfa["reachable_states"]:
        gnfa["transition_function"][state] = {}
        for alphabet in dfa["alphabets"]:
            next_state = dfa["transition_function"][state][alphabet]
            # appending only those which are not reachable from themselves from 
            if is_not_dead[next_state]:
                gnfa["transition_function"][state][alphabet] = next_state
                # gnfa["transition_function"][state] = dfa["transition_function"][state]

    # attach final states of dfs to final state of gnfa with epsilon transition
    for state in dfa["final_reachable_states"]:
        gnfa["transition_function"][state]["E"] = gnfa["final_states"][0]

    gnfa["transition_function"][gnfa["final_states"][0]] = {}

    #debug##########################################
    state_name = {}
    i = 0
    for state in gnfa["states"]:
        if state == "phi":
            state_name[state] = "\u03A6"
        else:
            state_name[state] = "q{}".format(i).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            i+=1
    ################################################

    for state_1 in gnfa["states"]:

        L[state_1] = {}
        for state_2 in gnfa["states"]:
            # if state_1 == state_2:
            #     L[state_1][state_2] = "E"
            # else:
            L[state_1][state_2] = ""
        for alphabet, next_state in gnfa["transition_function"][state_1].items():
            L[state_1][next_state] = union_regex(L[state_1][next_state], alphabet)
    # for chosen_state in gnfa["states"]:
    #     print("chosen: ", state_name[next_state])
    #     for alphabet, next_state in gnfa["transition_function"][chosen_state].items():
    #         print("$$",alphabet, state_name[next_state])
    
    
    visited = []

    print("-----------------------")

    for chosen_state in gnfa["states"]:
        
        print("chosen: ", state_name[chosen_state])
        for alphabet, next_state in gnfa["transition_function"][chosen_state].items():
            print("$$",alphabet, state_name[next_state])
    print("-----------------------")

    reachable_non_dead_states = filter(lambda x: is_not_dead[x], dfa["reachable_states"])

    # removing states one by one gnfa["states"]:
    for chosen_state in reachable_non_dead_states:
        # print(gnfa["transition_function"][chosen_state])
        print("chosen: ", state_name[chosen_state])
        for alphabet, next_state in gnfa["transition_function"][chosen_state].items():
            print("$$",alphabet, state_name[next_state])

        # for cleene star
        for alphabet, next_state in gnfa["transition_function"][chosen_state].items():
            if chosen_state == next_state:
                L[chosen_state][chosen_state] = union_regex(L[chosen_state][chosen_state], alphabet)
        print("-> ",L[chosen_state][chosen_state])

        if L[chosen_state][chosen_state] != "":
            L[chosen_state][chosen_state] = cleene_star_regex(L[chosen_state][chosen_state])
            print("-#> ",L[chosen_state][chosen_state])

            # for appending star with next values
            next_states =  list(gnfa["transition_function"][chosen_state].items())
            for alphabet, next_state in next_states:
                if chosen_state != next_state:
                    print("-2> ",L[chosen_state][next_state])
                    L[chosen_state][next_state] = concat_regex(L[chosen_state][chosen_state], L[chosen_state][next_state])
                    print("-3> ",L[chosen_state][next_state])
                    del gnfa["transition_function"][chosen_state][alphabet]
                    gnfa["transition_function"][chosen_state][L[chosen_state][next_state]] = next_state
                else:
                    del gnfa["transition_function"][chosen_state][alphabet]
                    

        # concatenating prev state of chosen state to next states of chosen state
        for prev_state in gnfa["states"]:
            print("States: ", state_name[prev_state], state_name[chosen_state])
            if prev_state != chosen_state:
                prev_next_states = list(gnfa["transition_function"][prev_state].items())

                for alphabet, next_state in prev_next_states:
                    print(alphabet, state_name[next_state])
                for alphabet, next_state in prev_next_states:
                    if next_state == chosen_state:
                        # L[prev_state][chosen_state] = alphabet
                        # connecting prev_state to next of chosen
                        new_strings = []
                        for chosen_state_alphabet, chosen_next_state in gnfa["transition_function"][chosen_state].items():
                            print("-##> ",L[prev_state][chosen_state], L[chosen_state][chosen_next_state] )
                            print("-##2> ",L[prev_state][chosen_next_state] )
                            L[prev_state][chosen_next_state] = concat_regex(L[prev_state][chosen_state] , L[chosen_state][chosen_next_state])
                            print("-##3> ", state_name[prev_state], L[prev_state][chosen_next_state], state_name[chosen_next_state] )
                            gnfa["transition_function"][prev_state][L[prev_state][chosen_next_state]] = chosen_next_state
                            new_strings.append(L[prev_state][chosen_next_state])
                        if alphabet not in new_strings:
                            del gnfa["transition_function"][prev_state][alphabet]
        ######################################################################3

        # # dealt with cleene star with self
        # for alphabet in gnfa["alphabets"]:
        #     if alphabet in gnfa["transition_function"][chosen_state].keys():
        #         if chosen_state == gnfa["transition_function"][chosen_state][alphabet]:
        #             L[chosen_state][chosen_state] = union_regex(L[chosen_state][chosen_state], cleene_star_regex(alphabet))
    
    for chosen_state in gnfa["states"]:
        print( gnfa["transition_function"][chosen_state])      
        
    print(L)
    print(L[gnfa["initial_state"]][gnfa["final_states"][0]])
    return L[gnfa["initial_state"]][gnfa["final_states"][0]]
    # print(gnfa["transition_function"][gnfa["initial_state"]])


def dfa_to_regex_3(dfa):
    L = {}

    # find dead states
    visited = []
    is_dead = {}

    def is_final(state):
        if state in is_dead.keys():
            return is_dead[state]
        if state in dfa["final_reachable_states"]:
            return True
        else:
            visited.append(state)
            res_a = False
            res_b = False
            next_state_a = dfa["transition_function"][state]["a"]
            if next_state_a not in visited:
                res_a = is_final(next_state_a)
            next_state_b = dfa["transition_function"][state]["b"]
            if next_state_b not in visited:
                res_b = is_final(next_state_b)
            return res_a | res_b
        return False



    for state in dfa["reachable_states"]:
        # tmp_state = state
        is_dead[state] = not is_final(state)
        
    print(is_dead)

    # make new start state
    gnfa = {}
    gnfa["initial_state"] = uuid.uuid4()
    gnfa["final_states"] =  [uuid.uuid4()]

    gnfa["states"] = [gnfa["initial_state"]]
    gnfa["states"].extend(dfa["reachable_states"])
    gnfa["states"].extend(gnfa["final_states"])

    gnfa["alphabets"] = ["a", "b", "E"]

    gnfa["transition_function"]= {}
    # attach initial state of gnfa to initial state of dfa with epsilon transition
    gnfa["transition_function"][gnfa["initial_state"]] = {"E": dfa["initial_state"]}

    # append rest of the transitions of dfa to gnfa
    for state in dfa["reachable_states"]:
        gnfa["transition_function"][state] = {}
        for alphabet in dfa["alphabets"]:
            next_state = dfa["transition_function"][state][alphabet]
            # appending only those which are not reachable from themselves from 
            if not is_dead[next_state]:
                gnfa["transition_function"][state][alphabet] = next_state
                # gnfa["transition_function"][state] = dfa["transition_function"][state]

    # attach final states of dfs to final state of gnfa with epsilon transition
    for state in dfa["final_reachable_states"]:
        gnfa["transition_function"][state]["E"] = gnfa["final_states"][0]

    gnfa["transition_function"][gnfa["final_states"][0]] = {}

    for state_1 in gnfa["states"]:

        # alphabets = dfa["alphabets"]
        # if state_1 in dfa["final_reachable_states"]:
        #     alphabets = gnfa["alphabets"]

        L[state_1] = {}
        for state_2 in gnfa["states"]:
            if state_1 == state_2:
                L[state_1][state_2] = "E"
            else:
                L[state_1][state_2] = "" # "phi"
            for alphabet in gnfa["alphabets"]:
                if alphabet in gnfa["transition_function"][state_1].keys():
                    if state_2 == gnfa["transition_function"][state_1][alphabet]:
                        L[state_1][state_2] = union_regex(L[state_1][state_2], alphabet)

    # print(len(dfa["reachable_states"]))
    # print(len(gnfa["states"]))
    # initial_state = gnfa["initial_state"]
    # final_state = gnfa["final_states"][0]
    # print(initial_state)
    # print(L[initial_state][initial_state])

    # i = 1
    for state in dfa["reachable_states"]:
        for state_1 in gnfa["states"]:
            for state_2 in gnfa["states"]:
                L[state_1][state_1] = union_regex(L[state_1][state_1], concat_regex(L[state_1][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_1])))
                L[state_2][state_2] = union_regex(L[state_2][state_2], concat_regex(L[state_2][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_2])))
                L[state_1][state_2] = union_regex(L[state_1][state_2], concat_regex(L[state_1][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_2])))
                L[state_2][state_1] = union_regex(L[state_2][state_1], concat_regex(L[state_2][state], concat_regex(cleene_star_regex(L[state][state]), L[state][state_1])))
                # # print(state_1,state_2)
                # print()
                # print(L)
                # print()
                # time.sleep(5)
                # print(i)
                # i+=1

    initial_state = gnfa["initial_state"]
    final_state = gnfa["final_states"][0]
    new_reg_exp = concat_regex(cleene_star_regex(L[initial_state][initial_state]), concat_regex(L[initial_state][final_state], cleene_star_regex( union_regex( concat_regex(L[final_state][initial_state], concat_regex(cleene_star_regex(L[initial_state][initial_state]), L[initial_state][final_state])) , L[final_state][final_state]) )))
    return new_reg_exp


if __name__=="__main__":
    reg_exp = "a(a+b)*b"
    reg_exp = "ab"
    # reg_exp = "(a+ab)(a+ab)*"
    reg_exp = "(a+b)*b"
    reg_exp = "a+(a+b)*a"

    nfa = regex_to_nfa(reg_exp)
    dfa = nfa_to_dfa(nfa)
    new_dfa = dfa_to_efficient_dfa(dfa)
    draw_dfa(new_dfa, "[Minimized] {}".format(reg_exp))
    new_reg_exp = dfa_to_regex_2(new_dfa)
    print(new_reg_exp)

    # print(union_regex("ab", "a"))
    # print(union_regex("", ""))