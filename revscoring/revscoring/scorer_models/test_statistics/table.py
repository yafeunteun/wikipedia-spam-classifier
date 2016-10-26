from collections import defaultdict

from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic


class table(ClassifierStatistic):
    """
    Constructs an accuracy generator.

    When applied to a test set, the `score()` method will return a `float`
    representing the proportion of correct predicitions.
    """

    @classmethod
    def score(self, scores, labels):
        predicteds = [s['prediction'] for s in scores]

        pairs = {}
        for pair in zip(labels, predicteds):
            pairs[pair] = pairs.get(pair, 0) + 1

        table = {}
        for (actual, predicted), count in pairs.items():
            if actual not in table:
                table[actual] = {}

            table[actual][predicted] = count

        return table

    def merge(self, tables):
        merged_table = defaultdict(lambda: defaultdict(int))

        for table in tables:
            for actual, p_table in table.items():
                for predicted, count in p_table.items():
                    merged_table[actual][predicted] += count

        return {
            actual: {predicted: count for predicted, count in p_table.items()}
            for actual, p_table in merged_table.items()}

    def format(cls, table, format="str"):

        if format == "str":
            return cls.format_str(table)
        elif format == "json":
            return table
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

    def format_str(cls, table_counts):
        possible = list(table_counts.keys())
        possible.sort()

        table_data = []
        for actual in possible:
            table_data.append(
                [(str(actual))] +
                [table_counts[actual].get(predicted, 0)
                 for predicted in possible]
            )

        table_str = tabulate(table_data,
                             headers=["~{0}".format(p) for p in possible])

        return "Table:\n" + \
               "".join("\t" + line + "\n" for line in
                       table_str.split("\n"))

TestStatistic.register("table", table)
