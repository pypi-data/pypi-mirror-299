import typing
from .base_payload import PayloadContainer


# This is a simplified version of WorkflowMappingPayloadContainer from database_facade. It will only allow for reads
class WorkflowMappingTimeBasedClusterLinesPayloadContainer(PayloadContainer):
    payloadPrefix = "WorkflowMapperTimeBasedClusterLines::"

    def __init__(
        self,
        id: typing.Optional[str] = None,
        workflowMappingHash: typing.Optional[str] = None,
    ) -> None:
        self.id: typing.Optional[str] = id
        self.workflowMappingHash: typing.Optional[str] = workflowMappingHash

    @staticmethod
    def fromPayload(
        payload_map: typing.Dict[str, typing.Any],
    ) -> typing.Union["WorkflowMappingTimeBasedClusterLinesPayloadContainer", None]:
        if "workflowMapperTimeBasedClusterLinesFlag" in payload_map.keys():
            if payload_map["workflowMapperTimeBasedClusterLinesFlag"]:
                # we have a WPE payload
                try:
                    # print(payload_map)
                    return WorkflowMappingTimeBasedClusterLinesPayloadContainer(
                        id=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterLinesPayloadContainer.payloadPrefix}id"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterLinesPayloadContainer.payloadPrefix}id"
                            in payload_map.keys()
                            else None
                        ),
                        workflowMappingHash=(
                            payload_map[
                                f"{WorkflowMappingTimeBasedClusterLinesPayloadContainer.payloadPrefix}workflowMappingHash"
                            ]
                            if f"{WorkflowMappingTimeBasedClusterLinesPayloadContainer.payloadPrefix}workflowMappingHash"
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
