# Copyright 2023 by Armoha.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Final, NoReturn, Self

from ... import core as c
from ... import utils as ut
from ...localize import _
from .epdoffsetmap import EPDOffsetMap
from .memberkind import BaseKind, MemberKind


class BaseMember(metaclass=ABCMeta):
    """Base descriptor class/mixin for EPDOffsetMap"""

    __slots__ = ()

    offset: Final[int]
    kind: Final[type[BaseKind]]
    __objclass__: type
    __name__: str

    def __init__(self, offset: int, kind: MemberKind) -> None:
        self.offset = offset  # type: ignore[misc]
        self.kind = kind.impl()  # type: ignore[misc]
        ut.ep_assert(offset % 4 + self.kind.size() <= 4, _("Malaligned member"))

    def _get_epd(self, instance):
        raise NotImplementedError

    def __set_name__(self, owner, name):
        self.__objclass__ = owner
        self.__name__ = name

    @abstractmethod
    def __get__(self, instance, owner=None):
        ...

    @abstractmethod
    def __set__(self, instance, value) -> None:
        ...


class StructMember(BaseMember):
    """Struct field member"""

    __slots__ = ("offset", "kind", "__objclass__", "__name__")

    def __init__(self, offset: int, kind: MemberKind) -> None:
        super().__init__(offset, kind)

    def _get_epd(self, instance: EPDOffsetMap):
        q, r = divmod(self.offset, 4)
        return instance._value + q, r

    def __get__(self, instance: EPDOffsetMap | None, owner=None):
        from .epdoffsetmap import EPDOffsetMap

        if instance is None:
            return self
        if isinstance(instance, EPDOffsetMap):
            epd, subp = self._get_epd(instance)
            return self.kind.cast(self.kind.read_epd(epd, subp))
        raise AttributeError

    def __set__(self, instance: EPDOffsetMap, value) -> None:
        from .epdoffsetmap import EPDOffsetMap

        if isinstance(instance, EPDOffsetMap):
            epd, subp = self._get_epd(instance)
            self.kind.write_epd(epd, subp, self.kind.cast(value))
            return
        raise AttributeError


class ArrayMember(BaseMember):
    """Parallel array member"""

    __slots__ = ("offset", "kind", "stride", "__objclass__", "__name__")

    def __init__(
        self, offset: int, kind: MemberKind, *, stride: int | None = None
    ) -> None:
        super().__init__(offset, kind)
        if stride is None:
            self.stride: int = self.kind.size()
        else:
            ut.ep_assert(
                self.kind.size() <= stride, "stride is greater than member size"
            )
            self.stride = stride

    def _get_epd(
        self, instance: EPDOffsetMap
    ) -> tuple[int | c.EUDVariable, int | c.EUDVariable]:
        value = instance._value
        if not isinstance(value, c.EUDVariable):
            epd, subp = divmod(self.offset + value * self.stride, 4)
            return ut.EPD(0) + epd, subp
        if self.stride == 4:
            return ut.EPD(self.offset) + value, self.offset % 4

        # lazy calculate multiplication & division
        q, r, update = instance._get_stride_cache(self.stride)
        update_start, update_restore, update_end = update

        nexttrg = c.Forward()
        c.RawTrigger(
            nextptr=update_start,
            actions=[
                c.SetNextPtr(update_start, update_restore),
                c.SetMemory(update_start + 348, c.SetTo, nexttrg),
                c.SetNextPtr(update_end, nexttrg),
            ],
        )
        nexttrg << c.NextTrigger()

        epd = ut.EPD(self.offset) + q
        if self.offset % 4 == 0:
            subp = r
        else:
            subp = self.offset % 4 + r
            if self.offset % 4 + (4 - self.stride) % 4 >= 4:
                c.RawTrigger(
                    conditions=subp.AtLeast(4),
                    actions=[subp.SubtractNumber(4), epd.AddNumber(1)],
                )
        return epd, subp

    def __get__(self, instance: EPDOffsetMap | None, owner=None):
        from .epdoffsetmap import EPDOffsetMap

        if instance is None:
            return self
        if isinstance(instance, EPDOffsetMap):
            epd, subp = self._get_epd(instance)
            return self.kind.cast(self.kind.read_epd(epd, subp))
        raise AttributeError

    def __set__(self, instance: EPDOffsetMap, value) -> None:
        from .epdoffsetmap import EPDOffsetMap

        if isinstance(instance, EPDOffsetMap):
            epd, subp = self._get_epd(instance)
            self.kind.write_epd(epd, subp, self.kind.cast(value))
            return
        raise AttributeError


class UnsupportedMember(BaseMember):
    """
    'Sorry, this EUD map is not supported' error is raised when it's accessed.

    '이 EUD 지도는 스타크래프트 리마스터와 호환되지 않습니다.' 오류가 발생합니다.
    """

    __slots__ = ("offset", "kind", "__objclass__", "__name__")

    def __get__(self, instance, owner=None) -> Self:
        if instance is None:
            return self
        raise ut.EPError(
            _(
                "StarCraft: Remastered does not support {}.{} "
                "and causes in-game errors."
            ).format(self.__objclass__, self.__name__)
        )

    def __set__(self, instance, value) -> NoReturn:
        raise ut.EPError(
            _(
                "StarCraft: Remastered does not support {}.{} "
                "and causes in-game errors."
            ).format(self.__objclass__, self.__name__)
        )


class NotImplementedMember(BaseMember):
    __slots__ = ("offset", "kind", "__objclass__", "__name__")

    def __get__(self, instance, owner=None) -> Self:
        if instance is None:
            return self
        raise ut.EPError(
            _("{} is not implemented for {}").format(
                self.__name__, self.__objclass__
            )
        )

    def __set__(self, instance, value) -> NoReturn:
        raise ut.EPError(
            _("{} is not implemented for {}").format(
                self.__name__, self.__objclass__
            )
        )
