import airweb


def test_medium():
    assert airweb.get(
        "https://medium.com/p/dca128e0202a", redirectors=[airweb.redirectors.medium]
    )
