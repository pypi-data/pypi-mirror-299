# -*- coding: utf-8 -*-

"""Base command for all Veld commands

"""

from typing import List
from typing import Optional
from typing import TypeVar

from wilderness import Command

from veld.exceptions import EmptyStreamError
from veld.stream_processor import BaseStreamProcessor
from veld.stream_processor import ForgivingStreamProcessor
from veld.stream_processor import NumericStreamProcessor

T = TypeVar("T")


class VeldCommand(Command):
    def register(self):
        self.add_argument(
            "file",
            help="File to read from (otherwise stdin)",
            nargs="?",
            description=(
                "Veld is primarily designed for processing input streams, "
                "but it can also be applied on a file of data, which can "
                "be supplied with this argument. By default Veld will read "
                "the input data from stdin."
            ),
        )
        group = self.add_argument_group(title="processing options")
        group.add_argument(
            "-e",
            "--encoding",
            help="Encoding of the input stream",
            default="utf-8",
            description=("Specify the encoding of the input stream."),
        )
        group.add_argument(
            "-f",
            "--flatten",
            help="Apply operation on flattened input",
            action="store_true",
            description=(
                "With multidimensional input (more than one value per line) "
                "the operation is normally conducted on each dimension "
                "independently. With the --flatten option, the input is "
                "flattened line-wise (RowMajor order) and the operation "
                "is conducted on the resulting one-dimensional stream."
            ),
        )
        group.add_argument(
            "-i",
            "--ignore",
            help="Ignore non-numeric values in the input stream",
            action="store_true",
        )
        group.add_argument(
            "-s",
            "--separator",
            help="Separator for values in the stream",
            description=(
                "Some of the Veld commands have support for "
                "multidimensional input data. The values on each line "
                "of the input stream are expected to be separated by this "
                "separator. By default, the tab character will be used as "
                "a separator."
            ),
            default="\t",
        )
        self._processing_args_group = group

    def _get_stream_processor(
        self, keep_text: bool = False
    ) -> BaseStreamProcessor:
        if keep_text:
            return ForgivingStreamProcessor(
                path=self.args.file,
                sep=self.args.separator,
                encoding=self.args.encoding,
                flatten=self.args.flatten,
                ignore_invalid=self.args.ignore,
            )
        return NumericStreamProcessor(
            path=self.args.file,
            sep=self.args.separator,
            encoding=self.args.encoding,
            flatten=self.args.flatten,
            ignore_invalid=self.args.ignore,
        )

    def _consume_stream(self, keep_text: bool = False) -> List[List[T]]:
        """Read the data stream into memory as a list of columns"""
        columns: Optional[List[List[T]]] = None
        value: T
        for row in self._get_stream_processor(keep_text=keep_text):
            for i, value in enumerate(row):
                if columns is None:
                    columns = []
                    for j in range(len(row)):
                        columns.append([])
                columns[i].append(value)
        if columns is None:
            raise EmptyStreamError()
        return columns
