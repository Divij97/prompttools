from collections import defaultdict


class PromptTestRunner:
    """
    Base class for prompt test runners.
    """

    def __init__(self):
        self.ran = defaultdict(bool)
        self.harnesses = dict()

    def run(self, *args, **kwargs):
        """
        Runs the test if it has not already been run.
        """
        key = str(args)
        if self.ran[key]:
            return key
        self.harnesses[key] = self._get_harness(*args, **kwargs)
        self.harnesses[key].prepare()
        self.harnesses[key].run()
        self.ran[key] = True
        return key

    def evaluate(self, key, metric_name, eval_fn, use_input_pairs):
        """
        Evaluates the test results.
        """
        self.harnesses[key].evaluate(metric_name, eval_fn, use_input_pairs)

    def rank(self, key, metric_name, is_average):
        """
        Uses evaluations to "rank" the template or system prompt.
        This creates an overall score (sum or average) across all
        test inputs, which can be compared against a threshold.
        """
        return self.harnesses[key].rank(metric_name, is_average)