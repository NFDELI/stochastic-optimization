import sys

sys.path.append("./")
from BaseClasses.SDPModel import SDPModel
from BaseClasses.SDPPolicy import SDPPolicy


class SellLowPolicy(SDPPolicy):
    # Maybe Theta is price range for policy.
    def __init__(self, model: SDPModel, policy_name: str = "SellLow", theta_low: float = 10):
        super().__init__(model, policy_name)
        self.theta_low = theta_low

    def get_decision(self, state, t, T):
        # Sell if price is lower than 'theta.low'.
        # Hold if price is higher than 'theta.low'.
        new_decision = {"sell": 1, "hold": 0} if state.price < self.theta_low else {"sell": 0, "hold": 1}

        # Sell if time frame has been reached.
        if t == T - 1:
            new_decision = {"sell": 1, "hold": 0}

        # 'new_decision' is a dictionary.
        return new_decision


class HighLowPolicy(SDPPolicy):
    def __init__(
        self, model: SDPModel, policy_name: str = "HighLow", theta_low: float = 10, theta_high: float = 30
    ):
        super().__init__(model, policy_name)
        self.theta_low = theta_low
        self.theta_high = theta_high

    def get_decision(self, state, t, T):
        new_decision = (
            # Sell if the price is lower than 'theta.low' OR higher than 'theta.high'
            {"sell": 1, "hold": 0}
            if state.price < self.theta_low or state.price > self.theta_high
            else {"sell": 0, "hold": 1}
        )

        # When time has reached, return a decision.
        if t == T - 1:
            new_decision = {"sell": 1, "hold": 0}

        return new_decision


class TrackPolicy(SDPPolicy):
    def __init__(self, model: SDPModel, policy_name: str = "Track", theta: float = 10):
        super().__init__(model, policy_name)
        self.theta = theta

    def get_decision(self, state, t, T):
        new_decision = (
            {"sell": 1, "hold": 0}
            if state.price >= state.price_smoothed + self.theta
            or state.price <= state.price_smoothed - self.theta
            else {"sell": 0, "hold": 1}
        )

        if t == T - 1:
            new_decision = {"sell": 1, "hold": 0}
        return new_decision
