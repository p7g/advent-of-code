from aoc import *

modules = {}
preds = {}

for line in data.splitlines():
    name, dests = line.split(" -> ")
    if name.startswith("%"):
        type_ = "%"
        name = name[1:]
    elif name.startswith("&"):
        type_ = "&"
        name = name[1:]
    else:
        type_ = name
    dests = dests.split(", ")
    modules[name] = (type_, dests)
    for dest in dests:
        preds.setdefault(dest, set()).add(name)


def simulate(states, i=0, yield_when_on=None):
    signals = [("broadcaster", False, "button")]
    while signals:
        new_signals = []
        for module, pulse, from_ in signals:
            num_pulses[pulse] += 1
            if module not in modules:
                continue
            type_, dests = modules[module]
            if type_ == "broadcaster":
                for dest in dests:
                    new_signals.append((dest, pulse, module))
            elif type_ == "%":
                if pulse:
                    continue
                state = states.get(module, False)
                new_state = not state
                states[module] = new_state
                for dest in dests:
                    new_signals.append((dest, new_state, module))
            elif type_ == "&":
                state = states.get(module)
                if state is None:
                    state = {pred: False for pred in preds[module]}
                    states[module] = state
                state[from_] = pulse
                pulse = not all(state.values())
                for dest in dests:
                    new_signals.append((dest, pulse, module))
                if yield_when_on and module in yield_when_on and pulse:
                    yield i + 1
                    yield_when_on.remove(module)
        signals = new_signals


states = {}
num_pulses = [0, 0]
for _ in range(1000):
    list(simulate(states))
print(num_pulses[0] * num_pulses[1])

x = set(preds["jq"])
y = []
states = {}
for i in count():
    if not x:
        break
    y.extend(simulate(states, i, x))
print(lcm(*y))
