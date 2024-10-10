from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PostXeetData(_message.Message):
    __slots__ = ("token", "text")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    token: str
    text: str
    def __init__(self, token: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class AuthData(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class AuthDetails(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class UserData(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class XeetData(_message.Message):
    __slots__ = ("id", "poster", "text", "liked", "likes")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSTER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LIKED_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    id: str
    poster: str
    text: str
    liked: bool
    likes: int
    def __init__(self, id: _Optional[str] = ..., poster: _Optional[str] = ..., text: _Optional[str] = ..., liked: bool = ..., likes: _Optional[int] = ...) -> None: ...

class Feed(_message.Message):
    __slots__ = ("feed",)
    FEED_FIELD_NUMBER: _ClassVar[int]
    feed: _containers.RepeatedCompositeFieldContainer[XeetData]
    def __init__(self, feed: _Optional[_Iterable[_Union[XeetData, _Mapping]]] = ...) -> None: ...

class LikeData(_message.Message):
    __slots__ = ("token", "xeet_id", "liked")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    XEET_ID_FIELD_NUMBER: _ClassVar[int]
    LIKED_FIELD_NUMBER: _ClassVar[int]
    token: str
    xeet_id: str
    liked: bool
    def __init__(self, token: _Optional[str] = ..., xeet_id: _Optional[str] = ..., liked: bool = ...) -> None: ...

class LikeUpdate(_message.Message):
    __slots__ = ("success", "likes")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    likes: int
    def __init__(self, success: bool = ..., likes: _Optional[int] = ...) -> None: ...
