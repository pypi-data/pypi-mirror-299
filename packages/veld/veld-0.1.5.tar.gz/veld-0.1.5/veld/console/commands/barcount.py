# -*- coding: utf-8 -*-

from collections import Counter

from typing import List
from typing import Tuple
from typing import Union

from veld.console.commands._plot import VeldPlotCommand


class BarCountCommand(VeldPlotCommand):
    def __init__(self) -> None:
        super().__init__(
            name="barcount",
            title="Create a histogram with bars for all unique values in the stream",
        )

    def register(self) -> None:
        super().register()
        mug = self.add_mutually_exclusive_group()
        mug.add_argument(
            "-r",
            "--relative",
            action="store_true",
            help="Plot relative counts (proportions) instead of counts",
        )
        mug.add_argument(
            "-p",
            "--percentage",
            action="store_true",
            help="Plot percentages instead of counts",
        )
        self.add_argument(
            "-w",
            "--width",
            help="Width of the bars (default: 0.8)",
            description=(
                "When there is one dimension of data in the input stream, "
                "this width is the width of each bar. When there are multiple "
                "dimensions, this width is shared between the bars."
            ),
            type=float,
            default=0.8,
        )

    def handle(self) -> int:
        all_values: List[List[Union[float, str]]] = self._consume_stream(
            keep_text=True
        )
        if all_values is None:
            return 1

        n_col = len(all_values)

        # say x = 1 and width = 0.6
        # one bar:
        #    x - 0.6/2 + 1 * 0.6 / 1 / 2       ->   [0.7, 1.3]
        # two bar:
        #    x - 0.6/2 + 1 * 0.6 / 2 / 2       ->   [0.7, 1.0]
        #    x - 0.6/2 + 3 * 0.6 / 2 / 2       ->   [1.0, 1.3]
        # three bar:
        #    x - 0.6/2 + 1 * 0.6 / 3 / 2       ->   [0.7, 0.9]
        #    x - 0.6/2 + 3 * 0.6 / 3 / 2       ->   [0.9, 1.1]
        #    x - 0.6/2 + 5 * 0.6 / 3 / 2       ->   [1.1, 1.3]
        # four bar:
        #    x - 0.6/2 + 1 * 0.6 / 4 / 2       ->   [0.7, 0.85]
        #    x - 0.6/2 + 3 * 0.6 / 4 / 2       ->   [0.85, 1.0]
        #    x - 0.6/2 + 5 * 0.6 / 4 / 2       ->   [1.0, 1.15]
        #    x - 0.6/2 + 7 * 0.6 / 4 / 2       ->   [1.15, 1.3]

        w = self.args.width

        counters = [Counter(column) for column in all_values]
        all_keys = sorted(
            set().union(*[counter.keys() for counter in counters]),
            key=_mixed_sort,
        )
        key_map = {key: i for i, key in enumerate(all_keys)}
        for i, counter in enumerate(counters):
            keys = sorted(counter.keys(), key=_mixed_sort)
            ys: List[float] = [counter[key] for key in keys]
            xs = [key_map[key] for key in keys]
            xs = [x - w / 2 + (2 * i + 1) * w / n_col / 2 for x in xs]
            if self.args.relative:
                ys = [y / sum(ys) for y in ys]
            elif self.args.percentage:
                ys = [y / sum(ys) * 100.0 for y in ys]
            self.plt.bar(xs, ys, width=w / n_col)

        self.plt.xticks(list(range(len(all_keys))), all_keys)

        self.set_plot_attributes()
        self.plt.show()
        return 0


def _mixed_sort(
    item: Union[int, float, str]
) -> Tuple[int, Union[int, float, str]]:
    return (0, item) if isinstance(item, (int, float)) else (1, item)
