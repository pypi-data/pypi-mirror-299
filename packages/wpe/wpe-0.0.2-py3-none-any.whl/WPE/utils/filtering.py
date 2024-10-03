from qdrant_client.models import ScoredPoint

import numpy as np
import typing


def deduplicateAndSort(
    points: typing.List[ScoredPoint],
):
    print(points[0].vector)
    P = np.array([p.vector for p in points])
    similarities = P @ P.T
    print(similarities)
    print(similarities.shape)
