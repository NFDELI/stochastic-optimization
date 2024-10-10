from copy import copy
from abc import ABC, abstractmethod
import pandas as pd
from . import SDPModel

# ABC means Abstract Base Class
class SDPPolicy(ABC):
    # 'model' determins which model we are using.
    # 'policy name' is a optional string to name the policy.
    def __init__(self, model: SDPModel, policy_name: str = ""):
        self.model = model
        self.policy_name = policy_name

        # Using a Dataframe to store the results of the policy runs.
        self.results = pd.DataFrame()

        # Holds the performance metrics after running the policy.
        self.performance = pd.NA

    @abstractmethod
    def get_decision(self, state, t, T):
        """
        Returns the decision made by the policy based on the given state.

        Args:
            state (namedtuple): The current state of the system.
            t (float): The current time step.
            T (float): The end of the time horizon / total number of time steps.

        Returns:
            dict: The decision made by the policy.
        """
        # Function is still empty. Will be define by inherited class.
        pass

    def run_policy(self, n_iterations: int = 1):
        """
        Runs the policy over the time horizon [0,T] for a specified number of iterations and return the mean performance.

        Args:
            n_iterations (int): The number of iterations to run the policy. Default is 1.

        Returns:
            None
        """
        # 'results_list' will be used to collect results from each iteration.
        result_list = []
        # Note: the random number generator is not reset when calling copy().
        # When calling deepcopy(), it is reset (then all iterations are exactly the same).
        for i in range(n_iterations):

            # A model_copy is used to ensure indepence of runs.
            model_copy = copy(self.model)
            model_copy.episode_counter = i
            model_copy.reset(reset_prng=False)
            state_t_plus_1 = None
            
            # While model is not finished.
            while model_copy.is_finished() is False:
                state_t = model_copy.state

                # 'decision_t' is the action taken based on the policy for a given state.
                decision_t = model_copy.build_decision(self.get_decision(state_t, model_copy.t, model_copy.T))

                # Logging
                # What is N, T and C_t_sum?
                results_dict = {"N": i, "t": model_copy.t, "C_t sum": model_copy.objective}

                #'._asdict()' converts the 'state_t', a tuple, into a dictionary with the keys are the field names of the name tuples and their values be the tuple's values.
                #'.update()' adds/updates/merges the keys and values from another dictionary.
                results_dict.update(state_t._asdict())
                results_dict.update(decision_t._asdict())

                # Add the results of each time step during the iteration.
                result_list.append(results_dict)

                # 'state_t_plus_1' holds the state of the model AFTER taking an action based on the current state.
                # The model transitions to the next state.
                state_t_plus_1 = model_copy.step(decision_t)
            # Model is reset afrer each while-loop iteration

            # 'N' [iteration] keeps track of how many times the policy has been run.
            # 'C_t_sum' [Cumulative Objective] represents a perfomance metric that accumulates over time.
            # each 'results_dict' stores different metrics at different times of t.
            results_dict = {"N": i, "t": model_copy.t, "C_t sum": model_copy.objective}

            # Ensures only valid states are logged.
            if state_t_plus_1 is not None:

                # Updates 'results_dict' with the details of the final state after the last decision has been applied.
                results_dict.update(state_t_plus_1._asdict())
            
            # The simulation results will be added to 'results_list'
            """
            Example outcome:
            result_list = [
                {"N": 0, "t": 0, "C_t sum": 50},
                {"N": 0, "t": 1, "C_t sum": 75},
                {"N": 0, "t": 2, "C_t sum": 100},
                {"N": 1, "t": 0, "C_t sum": 60},
                {"N": 1, "t": 1, "C_t sum": 85},
                {"N": 1, "t": 2, "C_t sum": 110},
            ]
            """
            # Capture the results after the while loop is completed after each Iteration (N), but it captures the final state after all time steps have been proceed in 'N'
            result_list.append(results_dict)

        # Logging
        # Create a Panda Frame based on 'result_list'
        self.results = pd.DataFrame.from_dict(result_list)

        # t_end per iteration
        # Creates a new column 't_end'
        # t_end will get the largest 't' value of each N iteration. (makes it easier to track end of t)
        self.results["t_end"] = self.results.groupby("N")["t"].transform("max")

        # performance of one iteration is the cumulative objective at t_end
        # 'self.performance' will be a dataframe that contains column 'N' and 'C_t sum' IF 't' is equal to 'T'
        self.performance = self.results.loc[self.results["t"] == self.results["t_end"], ["N", "C_t sum"]]

        # Enables index look up based on the value of 'N'
        self.performance = self.performance.set_index("N")

        # For reporting, convert cumulative objective to contribution per time
        # Creates a new column 'C_t' and it stores the differences between each C_t_sum values in each iteration 'N'
        self.results["C_t"] = self.results.groupby("N")["C_t sum"].diff().shift(-1)

        if self.results["C_t sum"].isna().sum() > 0:
            print(f"Warning! For {self.results['C_t sum'].isna().sum()} iterations the performance was NaN.")
        
        # Returns the average of the Cumulative sum [C_t sum]
        return self.performance.mean().iloc[0]
