from typing import Callable, List, Optional, TypeVar, Union, overload

from selectolax.lexbor import LexborHTMLParser as HTMLParser, LexborNode as Node

from .primp import Client
from .air_web import to_markdown

RedirectorF = Callable[[Node], Node]
Redirector = Union[RedirectorF, str]


def get(
    url: str,
    *,
    redirectors: List[Redirector] = [],
    ok_codes: list[int] = [],
    **kwargs,
) -> str:
    client = Client(
        **{"verify": False, "follow_redirects": True, "impersonate": "chrome_128"}
        | kwargs
    )
    res = client.get(url)
    assert res.status_code in ok_codes + [
        200
    ], f"Status code: {res.status_code}:\n{res.text_markdown}"

    parser = ok(HTMLParser(res.content).css_first("html"))

    for rd in redirectors:
        if isinstance(rd, str):
            parser = ok(parser.css_first(rd))
        else:
            parser = rd(parser)

    return to_markdown(parser.html or "(No content, blank)")


@overload
def redirector(o: str) -> str: ...


T = TypeVar("T", bound=RedirectorF)


@overload
def redirector(o: T) -> T: ...


def redirector(o: Redirector) -> Union[str, RedirectorF]:
    return o


def ok(node: Optional[Node]) -> Node:
    assert node
    return node


class redirectors:
    @staticmethod
    @redirector
    def medium(node: Node) -> Node:
        n = ok(node.css_first("article"))

        card_node = ok(node.css_first(".bn.bh.l"))
        card_info = to_markdown(card_node.html or "").replace("\n\n", " ")

        card_node.insert_before(card_info)
        card_node.decompose()

        bar_node = node.css("div.ab.cp")[1]
        bar_node.decompose()

        return n
