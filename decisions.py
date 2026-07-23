
def required_equity(pot_before_call, call):
    final_pot = pot_before_call + call
    return call / final_pot


def call_ev(equity, pot_before_call, call):
    final_pot = pot_before_call + call
    expected_return = equity * final_pot
    expected_profit = expected_return - call

    return expected_profit