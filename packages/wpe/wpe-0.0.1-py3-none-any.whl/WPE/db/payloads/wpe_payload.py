import typing
from .base_payload import PayloadContainer


# This is a simplified version of WorkflowMappingPayloadContainer from database_facade. It will only allow for reads
class WorkflowMappingPayloadContainer(PayloadContainer):
    payloadPrefix = "WorkflowMapper::"

    def __init__(
        self,
        ocrText: str = None,
        ocrTextHash: str = None,
        appTitle: str = None,
        windowTitle: str = None,
        timestamp: int = None,
        isCached: bool = None,
        isMerged: bool = None,
    ) -> None:
        self.ocrText: str = ocrText
        self.ocrTextHash: str = ocrTextHash
        self.appTitle: str = appTitle
        self.windowTitle: str = windowTitle
        self.timestamp: int = timestamp
        self.isCached: bool = isCached
        self.isMerged: bool = isMerged

    @staticmethod
    def fromPayload(
        payload_map: typing.Dict[str, typing.Any],
    ) -> typing.Union["WorkflowMappingPayloadContainer", None]:
        if "workflowMappingFlag" in payload_map.keys():
            if payload_map["workflowMappingFlag"]:
                # we have a WPE payload
                try:
                    # print(payload_map)
                    return WorkflowMappingPayloadContainer(
                        ocrText=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}ocrText"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}ocrText"
                            in payload_map.keys()
                            else None
                        ),
                        ocrTextHash=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}ocrTextHash"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}ocrTextHash"
                            in payload_map.keys()
                            else None
                        ),
                        appTitle=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}appTitle"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}appTitle"
                            in payload_map.keys()
                            else None
                        ),
                        windowTitle=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}windowTitle"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}windowTitle"
                            in payload_map.keys()
                            else None
                        ),
                        timestamp=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}timestamp"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}timestamp"
                            in payload_map.keys()
                            else None
                        ),
                        isCached=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}isCached"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}isCached"
                            in payload_map.keys()
                            else None
                        ),
                        isMerged=(
                            payload_map[
                                f"{WorkflowMappingPayloadContainer.payloadPrefix}isMerged"
                            ]
                            if f"{WorkflowMappingPayloadContainer.payloadPrefix}isMerged"
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
