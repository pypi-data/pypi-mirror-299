# -*- coding: utf-8 -*-

from typing import List
from typing import Optional

from veld.console.commands._base import VeldCommand
from veld.core.streamed_variance import StreamedVariance


class StandardDeviationCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="stdev",
            title="Compute the standard deviation of the input stream",
            extra_sections={
                "NOTES": (
                    "1. https://en.wikipedia.org/wiki/Standard_deviation#Uncorrected_sample_standard_deviation"
                )
            },
        )

    def register(self):
        super().register()
        self.add_argument(
            "-p",
            "--population",
            help="Compute the population standard deviation",
            description=(
                "By default the Veld stdev command computes an unbiased "
                "estimator of the sample standard deviation. If the data "
                "stream constitutes the entirety of a finite population, "
                "then you can use this flag to compute the uncorrected "
                "population standard deviation [1]."
            ),
            action="store_true",
        )

    def handle(self) -> int:
        svs: Optional[List[StreamedVariance]] = None

        for values in self._get_stream_processor():
            if svs is None:
                svs = [
                    StreamedVariance(population=self.args.population)
                    for _ in range(len(values))
                ]

            for i in range(len(values)):
                svs[i].update(values[i])

        svs = [] if svs is None else svs
        variances = [sv.stdev for sv in svs]
        print(self.args.separator.join(map(str, variances)))
        return 0
