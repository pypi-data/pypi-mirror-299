import typing
from .base_payload import PayloadContainer


# This is a simplified version of WorkflowMappingPayloadContainer from database_facade. It will only allow for reads
class WorkflowMappingTimeBasedClusterPayloadContainer(PayloadContainer):
    payloadPrefix = "WorkflowMapperTimeBasedCluster::"

    def __init__(
        self,
        id: typing.Optional[str] = None,
        year: typing.Optional[int] = None,
        month: typing.Optional[int] = None,
        day: typing.Optional[int] = None,
        summary: typing.Optional[str] = None,
        finalized: typing.Optional[bool] = None,
    ) -> None:
        self.id: typing.Optional[str] = id
        self.year: typing.Optional[int] = year
        self.month: typing.Optional[int] = month
        self.day: typing.Optional[int] = day
        self.summary: typing.Optional[str] = summary
        self.finalized: typing.Optional[bool] = finalized

    @staticmethod
    def fromPayload(
        payload_map: typing.Dict[str, typing.Any],
    ) -> typing.Union["WorkflowMappingTimeBasedClusterPayloadContainer", None]:
        if "workflowMapperTimeBasedClusterFlag" in payload_map.keys():
            if payload_map["workflowMapperTimeBasedClusterFlag"]:
                # we have a WPE payload
                try:
                    # print(payload_map)
                    return WorkflowMappingTimeBasedClusterPayloadContainer(
                        id=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}id"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}id"
                            in payload_map.keys()
                            else None
                        ),
                        year=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}year"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}year"
                            in payload_map.keys()
                            else None
                        ),
                        month=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}month"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}month"
                            in payload_map.keys()
                            else None
                        ),
                        day=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}day"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}day"
                            in payload_map.keys()
                            else None
                        ),
                        summary=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}summary"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}summary"
                            in payload_map.keys()
                            else None
                        ),
                        finalized=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}finalized"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterPayloadContainer.payloadPrefix}finalized"
                            in payload_map.keys()
                            else None
                        ),
                    )
                except Exception as e:
                    # An error occured while trying to access some specific payload item
                    return None
            else:
                # WPE payload is empty
                return None
        else:
            # this shouldn't happen
            return None
