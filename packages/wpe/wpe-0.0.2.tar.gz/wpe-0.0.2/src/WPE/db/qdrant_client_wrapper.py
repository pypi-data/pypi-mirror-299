import qdrant_client as qdrant
from qdrant_client.models import (
    Filter,
    FieldCondition,
    Range,
    MatchValue,
    Record,
    QueryResponse,
    ScoredPoint,
)

import typing
import numpy as np


# This is a wrapper around our qdrant db
class QdrantClientWrapper:
    def __init__(self, host: str = "localhost", grpc_port: int = 6334):
        self.client: qdrant.QdrantClient = qdrant.QdrantClient(
            host=host, grpc_port=grpc_port, prefer_grpc=True
        )

        self.points = []
        self.unique_point_ids = set()
        self.offset = None

    def fetch(
        self,
        collection_name: str,
    ) -> typing.List[Record]:
        new_fetched_points = []

        points, offset = self.client.scroll(
            collection_name=collection_name,
            limit=1000,
            offset=self.offset,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="workflowMappingFlag",
                        match=MatchValue(value=True),
                    ),
                ],
            ),
        )
        # get rid of points that we already have
        points = [p for p in points if p.id not in self.unique_point_ids]

        # add new points to our list + add their ids to our uniqe id set
        self.points += points
        new_fetched_points += points
        for p in points:
            self.unique_point_ids.add(p.id)

        while offset is not None:
            self.offset = offset

            points, offset = self.client.scroll(
                collection_name=collection_name,
                limit=1000,
                offset=self.offset,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="workflowMappingFlag",
                            match=MatchValue(value=True),
                        ),
                    ],
                ),
            )
            # get rid of points that we already have
            points = [p for p in points if p.id not in self.unique_point_ids]

            # add new points to our list + add their ids to our uniqe id set
            self.points += points
            new_fetched_points += points
            for p in points:
                self.unique_point_ids.add(p.id)

        print(f"Fetched {len(new_fetched_points)} new points!")
        return new_fetched_points

    def fetchClusters(
        self,
        collection_name: str,
    ) -> typing.List[Record]:
        points, _ = self.client.scroll(
            collection_name=collection_name,
            limit=1000,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="workflowMapperTimeBasedClusterFlag",
                        match=MatchValue(value=True),
                    ),
                ],
            ),
        )
        return points

    def fetchClustersLines(
        self,
        collection_name: str,
    ) -> typing.List[Record]:
        points, _ = self.client.scroll(
            collection_name=collection_name,
            limit=10000,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="workflowMapperTimeBasedClusterLinesFlag",
                        match=MatchValue(value=True),
                    ),
                ],
            ),
        )
        return points

    def fetchAndProcess(
        self,
        collection_name: str,
        process_fn: typing.Callable,
        batch_size: int = 32,
    ) -> typing.Any:
        new_fetched_points = self.fetch(collection_name=collection_name)
        return process_fn(new_fetched_points)

    def query(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        limit: int = 10,
    ) -> typing.List[ScoredPoint]:
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="workflowMappingFlag",
                        match=MatchValue(value=True),
                    ),
                ],
            ),
            with_payload=True,
            with_vectors=True,
            limit=limit,
        )
