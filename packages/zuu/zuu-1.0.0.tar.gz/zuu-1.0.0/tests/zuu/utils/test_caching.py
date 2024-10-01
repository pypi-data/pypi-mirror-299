
def test_caching():
    from zuu.utils.caching import GitCacher

    gc = GitCacher()
    gc.add("https://github.com/ZackaryW/zugen-resources.git")
    w = gc.get("template.tex", fuzzyMatch=True)
    assert "awe2024" in w