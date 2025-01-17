from __future__ import print_function

import os
import json
import grpc
import re
import hashlib

from copy import copy

from . import server_pb2
from . import server_pb2_grpc

MAX_MESSAGE_LENGTH = 10485760 * 10
THEOREM_SEPARATOR = "<THM_SEP>"

# Class to store Isabelle lemmas and hypotheses
class IsabelleLemma(object):
    def __init__(self, name: str, dfn: str) -> None:
        self.name = name # The full lemma name
        self.dfn = dfn # The abridged lemma name and defn
    
    def __str__(self) -> str:
        return f"{self.name}: {self.dfn}"

def create_stub(port=9000):
    channel = grpc.insecure_channel('localhost:{}'.format(port),
                                    options=[('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                                             ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)])
    return server_pb2_grpc.ServerStub(channel)

def initialise_env(port=8000,
                   isa_path="~/Isabelle2022",
                   theory_file_path="~/Isabelle2022/src/HOL/Library/Discrete.thy",
                   working_directory="~/Isabelle2022/src/HOL/Library", 
                   debug=False):
    isa_path = os.path.abspath(os.path.expanduser(isa_path))
    theory_file_path = os.path.abspath(os.path.expanduser(theory_file_path))
    working_directory = os.path.abspath(os.path.expanduser(working_directory))
    return PisaEnv(port=port, isa_path=isa_path, starter_string=theory_file_path, working_directory=working_directory, debug=debug)


class PisaEnv:
    def __init__(self, 
        port=9000, 
        isa_path="/Applications/Isabelle2020.app/Isabelle",
        starter_string="theory Test imports Complex_Main begin",
        working_directory="/Users/qj213/Projects/afp-2021-02-11/thys/Functional-Automata",
        debug=False
    ):
        self.port = port
        self.isa_path = isa_path
        self.starter_string = starter_string
        self.working_directory = working_directory
        self.debug = debug

        self.stub = None
        self.obs_string = None
        self.successful_starting = False
        self.reset()

    def reset(self):
        self.stub = create_stub(port=self.port)
        try:
            self.stub.InitialiseIsabelle(server_pb2.IsaPath(path=self.isa_path)).message
            self.stub.IsabelleWorkingDirectory(server_pb2.IsaPath(path=self.working_directory)).message
            self.stub.IsabelleContext(server_pb2.IsaContext(context=self.starter_string)).message
            self.successful_starting = True
        except Exception as e:
            # print("Failure at initialising Isabelle process.\n"
            #       "Make sure the path your provide is where the Isabelle executable is.")
            # print(e)
            pass
        return f"Starting is successful: {self.successful_starting}"

    def step(self, old_name, step, new_name, delete_old_state=False) -> str:
        '''
        :param old_name: the name of the old state
        :param step: the step to take
        :param new_name: the name of the new state
        :param delete_old_state: if true, delete the old state
        :return: the string of the new state
        I recommend not deleting the default state "default" as it is the starting state.
        '''
        obs_string = "Step error"
        try:
            obs_string = self.stub.IsabelleCommand(
                server_pb2.IsaCommand(command=f"<apply to top level state> {old_name} <apply to top level state> {step} <apply to top level state> {new_name}")).state
            if delete_old_state:
                self.stub.IsabelleCommand(server_pb2.IsaCommand(command=f"<delete> {old_name}"))
                print(f"Deleted old state with name: {old_name}")
        except Exception as e:
            print("***Something went wrong***")
            print(e)
        return obs_string

    def is_finished(self, name_of_tls):
        returned_string = self.post(f"<is finished> {name_of_tls}").strip()
        if returned_string.startswith("t"):
            return True
        else:
            return False

    def reward(self, done):
        if done:
            return 1
        else:
            return 0

    def get_premises(self, name_of_tls, theorem_name, theorem_proof_string):
        message = f"<get dependent theorems>{name_of_tls}<get dependent theorems>{theorem_name}<get dependent theorems>{THEOREM_SEPARATOR}"
        # print(f"Get dependent theroem string: {message}")
        returned_string = self.post(message)
        # print(f"Returned string: {returned_string}")
        premises = returned_string.split(THEOREM_SEPARATOR)
        premises = [premise.strip() for premise in premises]
        # print(premises)
        # print("premises raw", premises)
        # print(f"Returned premises: {'||'.join(premises)}")

        # Function to break down the proof string
        def further_break(chunks, separator=None):
            new_chunks = []
            for chunk in chunks:
                new_chunks.extend(chunk.split(separator))
            return new_chunks

        # Break down the proof string into chunks which might be premises
        possible_premise_chunks = further_break([theorem_proof_string])
        # print("First filter", possible_premise_chunks)
        legit_separators = [",", "(", ")", "[", "]", "{", "}", ":", '"', "<", ">", "\\"]
        for separtor in legit_separators:
            possible_premise_chunks = further_break(possible_premise_chunks, separtor)
        # print("Second filter", possible_premise_chunks)
        possible_premise_chunks = set(chunk.strip() for chunk in possible_premise_chunks)
        # print("Third filter", possible_premise_chunks)
        
        
        # Only include theorems that are in the proof string
        explicit_premises = []
        for premise in premises:
            premise_divisions = premise.split(".")
            for i in range(len(premise_divisions)):
                possible_way_to_refer_to_premise = ".".join(premise_divisions[i:])
                # print("possible_way", possible_way_to_refer_to_premise)
                if possible_way_to_refer_to_premise in possible_premise_chunks:
                    explicit_premises.append(premise)
                    break

        explicit_premises = [premise for premise in explicit_premises if premise.strip()]
        # print(theorem_name, theorem_proof_string, explicit_premises)
        # print("*"*100)
        return explicit_premises

    def get_fact_definition(self, name_of_tls, fact_name):
        message = f"<get fact definition>{name_of_tls}<get fact definition>{fact_name}"
        # print(f"Get fact definition: {message}")
        returned_string = self.post(message)
        # print(f"Returned definition: {returned_string}")
        return returned_string

    def get_premises_and_their_definitions(self, full_name, only_name, proof_body, debug=False):
        if debug: print("-1")
        self.initialise()
        if debug: print("0")
        # Getting unique name and clone the top level there
        tls_unique_name = str(hashlib.sha256(proof_body.encode("utf-8")).hexdigest())
        tls_unique_name = ''.join(filter(str.isalpha, tls_unique_name))
        # decorated_name = only_name.format(tls_unique_name)
        self.clone_to_new_name(tls_unique_name)
        if debug: print(0.5, "post clone")
        # Substitute proof
        # if not only_name.strip():
        #     sub_proof = f"<allow more time> theorem {proof_body}"
        # else:
        #     sub_proof = f"<allow more time> theorem {full_name}: {proof_body}"
        # if debug: print("1", sub_proof)
        # self.step_to_top_level_state(sub_proof, tls_unique_name, tls_unique_name)
        if debug: print("2, stepping")
        premises = self.get_premises(tls_unique_name, only_name, proof_body)
        if debug: print("3", premises)
        premises_and_their_definitions = [(premise, self.get_fact_definition(tls_unique_name, premise)) for premise in premises]
        if debug: print("4", premises_and_their_definitions)
        self.post(f"<delete> {tls_unique_name}")
        return premises_and_their_definitions

    # def get_premises_and_their_definitions(self, full_theorem_def, theorem_name, theorem_proof_string):
    #     # print("Get to end: " + self.proceed_until_end_of_theorem_proof(full_theorem_def))
    #     self.initialise()
    #     premises = self.get_premises("default", theorem_name, theorem_proof_string)
    #     # print(premises)
    #     premises_and_their_definitions = [(premise, self.get_fact_defintion("default", premise)) for premise in premises]
    #     return premises_and_their_definitions

    def proceed_until_end_of_theorem_proof(self, theorem_name):
        message = f"<accumulative_step_to_theorem_end> {theorem_name}"
        return self.post(message)

    def accumulative_step_before_theorem_starts(self, theorem_name):
        message = f"<accumulative_step_before_theorem_starts> {theorem_name}"
        return self.post(message)
    
    def accumulative_step_through_a_theorem(self):
        message = f"<accumulative_step_through_a_theorem>"
        return self.post(message)

    def step_to_top_level_state(self, action, tls_name, new_name):
        # last_obs_string = self.stub.IsabelleCommand(server_pb2.IsaCommand(command=f"<get state> {tls_name}")).state
        obs_string = "Step error"
        try:
            obs_string = self.post(f"<apply to top level state> {tls_name} <apply to top level state> {action} <apply to top level state> {new_name}")
            # print(obs_string)
        except Exception as e:
            print("***Something went wrong***")
            print(e)

        if "error" in obs_string:
            done = False
        else:
            done = self.is_finished(new_name)
        # done = True if ("subgoal" in last_obs_string and "subgoal" not in obs_string) else False
        return obs_string, self.reward(done), done, {}
    
    # Attempts to run sledgehammer on the current proof state
    def apply_hammer(self, tls_name, new_name):
        return self.step(tls_name, 'normalhammer', new_name)
    
    # Does not seem to work
    def get_all_defns(self, theorem_name):
        message = f"<get all definitions> {theorem_name}"
        return self.post(message)

    # Parse facts and defs and extract the lemma names
    def parse_lemma_content(self, tls_name, message: str):
        if not message.strip():
            return []
        sep = message.split('<SEP>')
        lemmas = [IsabelleLemma(lemma.split('<DEF>')[0].strip(), lemma.split('<DEF>')[1].strip()) for lemma in sep]
        return lemmas

    # Get local hypotheses
    def get_local_lemmas(self, tls_name):
        message = f"<local facts and defs> {tls_name}"
        return self.parse_lemma_content(tls_name, self.post(message))
    
    # Get global lemmas (may be from imports)
    def get_global_lemmas(self, tls_name):
        message = f"<global facts and defs> {tls_name}"
        return self.parse_lemma_content(tls_name, self.post(message))
    
    # Local + global lemmas
    def get_total_lemmas(self, tls_name):
        message = f"<total facts and defs> {tls_name}"
        return self.parse_lemma_content(tls_name, self.post(message))
    
    # Get the proof state string (this + goals)
    def get_state(self, tls_name):
        message = f"<get state> {tls_name}"
        return self.post(message)

    def proceed_after(self, line_string):
        return self.post(f"<proceed after> {line_string}")

    def initialise(self):
        return self.post("<initialise>")

    def clone_to_new_name(self, new_name):
        return self.post(f"<clone> default <clone> {new_name}")

    def post(self, action):
        if self.debug: print(action)
        returned = self.stub.IsabelleCommand(server_pb2.IsaCommand(command=action)).state
        if self.debug: print(returned)
        return returned

    def proceed_to_line(self, line_stirng, before_after):
        assert before_after in ["before", "after"]
        try:
            command = f"<proceed {before_after}> {line_stirng}"
            # print(command)
            message = self.stub.IsabelleCommand(server_pb2.IsaCommand(command=command)).state
            # print(message)
        except Exception as e:
            print("Failure to proceed before line")
            print(e)

    def proceed_until_end(self):
        return self.post("<proceed until end>")


def parsed_json_to_env_and_dict(path_to_json, afp_path, port=9000, isa_path="/Applications/Isabelle2020.app/Isabelle"):
    save_dict = json.load(open(path_to_json))
    project = save_dict["project"]
    wd = os.path.join(afp_path, "thys", project)
    segments = save_dict["segments"]
    # Find starter string
    starter_string = None
    for line in segments:
        if line.strip().startswith("theory"):
            starter_string = " ".join(line.strip().split("\n"))
            break
    assert starter_string
    # print(port, isa_path, starter_string, wd, segments)
    return PisaEnv(port=port, isa_path=isa_path,
                     starter_string=starter_string,
                     working_directory=wd), save_dict



if __name__ == '__main__':
    env = initialise_env(
        8001, 
        "/home/qj213/Isabelle2021", 
        "/home/qj213/afp-2021-10-22/thys/Real_Impl/Real_Impl_Auxiliary.thy", 
        "/home/qj213/afp-2021-10-22/thys/Real_Impl"
    )
    env.proceed_to_line('end', 'before')
    env.initialise()
    env.step_to_top_level_state('lemma primes_infinite: "\<not> (finite {(p::nat). prime p})"', "default", "test")
    print(env.step_to_top_level_state('sledgehammer', 'test', 'test1'))
    print(env.step_to_top_level_state('delhammer primes_infinite', 'test', 'test2'))
    print(env.step_to_top_level_state('delhammer primes_infinite,bigger_prime', 'test', 'test3'))
