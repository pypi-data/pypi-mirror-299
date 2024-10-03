# 🛫 air_web

A lightweight package for crawling the web with the minimalist of code.

```python
from air_web import get

# Crawl example.com and convert to Markdown
get("https://example.com")
```

## 🤨 Why & how
This is proof that web crawling can be done simply and at the highest level of API. No need to install the required 102 dependencies for one feature, no need to create a lot of class instances in order to get something up and running. With a simple `get()`, you get almost everything from the Internet.

`air_web` uses PyO3 as backend, utilizing the `html2text` crate for the `to_markdown` function, as well as some `.pyi` code to get everything typed nicely.

For the Python side, I used `primp` for browser fingerprint impersonation and `selectolax` for selecting HTML nodes.

## 🔄 Redirectors
Redirectors are used to redirect the HTML selector to one specific node to tidy up the results. For example, if the page has navbars, we can select the main content part to skip it through (if the nav isn't important).

`air_web` comes with a pre-built redirector for [Medium](https://medium.com) posts, you can pass it to the `get()` function via `redirectors=[...]` to get a cleaner result for posts:

```python
from air_web import redirectors

get(
  "https://medium.com/p/post-id-here",
  redirectors=[
    redirectors.medium,  # skip footers, navs, and straight to the post
  ]
)
```

**📝 Note**: The reason why the `redirectors` argument takes a list is that I want to make it sequential, meaning you can add multiple redirectors at once from other providers or custom ones made by you!

### ⚡️ Custom redirectors
You can create a custom redirector via functions or string literals containing a CSS selector. Below is an example that selects an element with the class `.article` and is inside of the `main` tag.

**🖱️ CSS selectors**:
```python
from air_web import Redirector  # type

MY_REDIRECTOR: Redirector = "main .article"  # CSS
```

Alternatively, you can use functions to manipulate the HTML nodes to clean everything up. Below is an example that removes advertisements from the node.

**🏭 Functional selectors**:
```python
from air_web import (
  Node,       # an HTML node
  ok,         # indicates the node exists and is not None
  redirector  # a decorator for typing (optional)
)

@redirector
def my_redirector(node: Node):
  main = ok(node.css_first("main"))

  # Remove advertisement
  ad = ok(main.css_first(".advertisement"))
  ad.decompose()

  return main
```

## 📖 Docs

### <kbd>def</kbd> get()

```python
def get(
    url: str,
    *,
    redirectors: List[Redirector] = [],
    ok_codes: list[int] = [],
    **kwargs,
) -> str: ...
```

Sends an HTTP GET request to the specified website and returns the Markdown result.

**Args**:
- `url` (str): The URL to fetch.
- `redirectors` (list\[Redirector]): A list of redirectors for indexing into or manipulating specific nodes before converting the HTML to Markdown. See the "Redirectors" section.
- `ok_codes` (list\[int]): A list of OK codes indicating the success status. Even if provided custom ones or not, the code `200` is always on the list.

## <kbd>def</kbd> to_markdown()

```python
def to_markdown(t: str) -> str: ...
```

Converts HTML to Markdown. (`src/lib.rs`)
