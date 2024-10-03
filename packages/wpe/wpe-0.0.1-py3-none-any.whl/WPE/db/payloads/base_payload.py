import typing


# This is a simplified version of WorkflowMappingPayloadContainer from database_facade. It will only allow for reads
class PayloadContainer:
    payloadPrefix: str

    @staticmethod
    def fromPayload(
        payload_map: typing.Dict[str, typing.Any],
    ) -> typing.Union["PayloadContainer", None]:
        raise NotImplementedError("Not implemented!")
