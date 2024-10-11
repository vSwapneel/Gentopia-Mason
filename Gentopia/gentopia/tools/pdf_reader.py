from typing import AnyStr
from gentopia.tools.basetool import *
import urllib.request
import PyPDF2
import io


class PdfReaderArgs(BaseModel):
    query: str = Field(..., description="a link to the paper")


class PdfReader(BaseTool):
    """Tool that adds the capability to query the Google search API."""

    name = "pdf_reader"
    description = ("A pdf reader reading the pdf."
                   "Input: pdf url")

    args_schema: Optional[Type[BaseModel]] = PdfReaderArgs

    def _run(self, query: AnyStr) -> str:
        req = urllib.request.Request(
            query, headers={'User-Agent': "Magic Browser"})
        file = urllib.request.urlopen(req).read()
        file_bytes = io.BytesIO(file)
        pdfdoc = PyPDF2.PdfReader(file_bytes)
        return "\n\n".join(pdfdoc.pages[i].extract_text() for i in range(len(pdfdoc.pages)))

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PdfReader()._run("https://dl.acm.org/doi/pdf/10.1145/3650212.3680328")
    #print(ans)
