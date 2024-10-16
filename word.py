from __future__ import annotations
from layer.layer import CanonLayer, Layer

class CanonWord:
    def __init__(self, w: Word) -> None:
        self.__layers: list[CanonLayer] = []
        self.__iter_index = -1
        # TODO: don't copy these
        word_layers = []
        word_layers.extend(w)
        for layer in reversed(word_layers):
            self.__layers.insert(0, CanonLayer(layer))

    def __iter__(self) -> Word:
        self.__iter_index = 0
        return self

    def __next__(self) -> Layer:
        if self.__iter_index >= len(self.__layers):
            raise StopIteration
        next_layer = self.__layers[self.__iter_index]
        self.__iter_index += 1
        return next_layer

    def __repr__(self) -> str:
        return f"CanonWord({self.__layers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CanonWord):
            return False
        return list(iter(self)) == list(iter(other))


class Word:
    def __init__(self) -> None:
        self.__layers = []
        self.__iter_index = -1

    # TODO: keep track of the above braid
    # and construct the Layer from a Knit
    # and the Braid
    def append_layer(self, l: Layer) -> None:
        self.__layers.append(l)

    def __iter__(self) -> Word:
        self.__iter_index = 0
        return self

    def __next__(self) -> Layer:
        if self.__iter_index >= len(self.__layers):
            raise StopIteration
        next_layer = self.__layers[self.__iter_index]
        self.__iter_index += 1
        return next_layer

    def __repr__(self) -> str:
        return f"Word({self.__layers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return list(iter(self)) == list(iter(other))
