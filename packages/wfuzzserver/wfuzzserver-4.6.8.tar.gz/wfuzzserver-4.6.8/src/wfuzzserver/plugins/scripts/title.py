from wfuzzserver.plugin_api.base import BasePlugin
from wfuzzserver.externals.moduleman.plugin import moduleman_plugin


@moduleman_plugin
class title(BasePlugin):
    name = "title"
    author = ("Xavi Mendez (@xmendez)",)
    version = "0.1"
    summary = "Parses HTML page title"
    description = ("Parses HTML page title",)
    category = ["info", "passive"]
    priority = 99

    parameters = ()

    def __init__(self):
        BasePlugin.__init__(self)

    def validate(self, fuzzresult):
        return True

    def process(self, fuzzresult):
        soup = fuzzresult.history.get_soup()
        title = soup.title.string if soup.title else ""

        if (
            title != ""
            and "title" not in self.kbase
            or title not in self.kbase["title"]
        ):
            self.kbase["title"] = title
            self.add_result("title", "Page title", title)
