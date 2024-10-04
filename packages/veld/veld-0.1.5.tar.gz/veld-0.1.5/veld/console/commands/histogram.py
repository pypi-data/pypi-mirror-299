# -*- coding: utf-8 -*-

import sys

from typing import List

from veld.console.commands._plot import VeldPlotCommand
from veld.exceptions import StreamProcessingError


class HistogramCommand(VeldPlotCommand):
    def __init__(self) -> None:
        super().__init__(
            name="histogram",
            title="Plot a histogram of the values in the data stream",
        )

    def register(self) -> None:
        super().register()
        self.add_argument(
            "-b", "--bins", help="Number of bins in the histogram", type=int
        )
        self.add_argument(
            "--density",
            action="store_true",
            help="Create a density plot",
            description=(
                "Create a density plot such that the area under the "
                "histogram integrates to 1."
            ),
        )
        self.add_argument(
            "--cumulative",
            action="store_true",
            help="Make the histogram bars cumulative",
            description=(
                "In cumulative mode, the height of each bar corresponds to "
                "the number of values in that bin plus all of the preceding "
                "ones. This can be combined with the --density option such "
                "that the last bar will equal 1."
            ),
        )
        self.add_argument(
            "--stacked",
            action="store_true",
            help="Stack bars for multidimensional data",
            description=(
                "With multidimensional data, stack the bars on top of "
                "each other. This differs from the default behavior where "
                "the bars are arranged side by side."
            ),
        )

    def handle(self) -> int:
        try:
            all_values: List[List[float]] = self._consume_stream()
        except StreamProcessingError:
            print(
                "ERROR: Failed to parse some values in the stream, note that "
                "histogram is meant for numerical values. Use barcount for "
                "non-numerical histograms.",
                file=sys.stderr,
            )
            raise

        self.plt.hist(
            all_values,
            bins=self.args.bins,
            cumulative=self.args.cumulative,
            density=self.args.density,
            stacked=self.args.stacked,
        )
        self.set_plot_attributes()
        self.plt.show()
        return 0
