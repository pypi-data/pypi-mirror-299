"""oviond tap class."""

from typing import List

from singer_sdk import Tap, Stream

from singer_sdk import typing as th  # JSON schema typing helpers

from tap_oviond.streams import oviondStream, CommentsStream


STREAM_TYPES = [CommentsStream]


class Tapoviond(Tap):
    """oviond tap class."""

    name = "tap-oviond"

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
