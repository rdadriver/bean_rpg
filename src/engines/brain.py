import json

"""
brain.py

A simple neural network
that is used to make decisions
such as the opponents next move
in the duelling.
"""

weights_preset = [
    [2, 3, 3, 0.5, 3, 1, 1, 3, 1, 0.5, 1.5, 0.5],
    [2, 3, 0.5, 3, 3, 1, 1, 3, 1, 1.5, 0.5, 0.5],
    [0.5, -1.5, 1, 1, -0.5, 3, 3, -1.5, 2, 1.5, 1.5, 3],
    [-1, -2, 1, 1, -0.5, 0.5, 0.5, -4, 3, 1, 1, 3]
]
with open("src/saves/training_data.json", 'r') as infile:
    scenarios = json.load(infile)["scenarios"]


class Brain:

    def __init__(self, inputs, outputs):

        self.inputs = inputs
        self.outputs = outputs

        self.weights = weights_preset  # [[random.uniform(-1.0, 1.0) for n in range(inputs)] for m in range(outputs)]
        self.bias = [0 for n in range(outputs)]

    def get_output(self, in_data):

        out_data = [sum([in_data[n]*weights_preset[x][n] for n in range(self.inputs)]) for x in range(self.outputs)]
        return out_data.index(max(out_data))


if __name__ == "__main__":
    test_brain = Brain(12, 4)

    print("Running test scenarios")
    n = 0
    c = 0
    for s in scenarios:
        n += 1

        o = test_brain.get_output(s[0])

        if int(s[1]) == o:
            c += 1

        print("Scenario {}: {}. Expected outcome: {}".format(n, o, s[1]))

    print("Success rate: {}".format(c/n*100))
