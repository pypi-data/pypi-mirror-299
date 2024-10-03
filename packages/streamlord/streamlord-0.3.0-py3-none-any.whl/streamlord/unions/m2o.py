import typing
import collections

T = typing.TypeVar('T')
InjectedKey = str
IndexKey = str


class M2OUnion(typing.Generic[T]):
    def __init__(
        self,
        stream: collections.abc.Iterable[T],
        index_key: str
    ):
        self._stream = stream
        self._index_key = index_key
        self._injections = {}

    def inject(
        self,
        stream: collections.abc.Iterable[T],
        index_key: InjectedKey,
        injected_key: InjectedKey,
        remove_index_key: bool = True
    ):
        self._injections[injected_key] = collections.defaultdict(list)
        for item in stream:
            index_value = item[index_key]
            if remove_index_key:
                item = {key: value for key, value in item.items() if key != index_key}
            self._injections[injected_key][index_value].append(item)
        return self

    def get(self) -> collections.abc.Generator[T]:
        for item in self._stream:
            for injection_key, injection_data in self._injections.items():
                item[injection_key] = injection_data[item[self._index_key]]
            yield item
