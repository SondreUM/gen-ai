import config
from pathlib import Path
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.docstore.document import Document

def parse_HTML():
    """Parse the data collected by the crawler"""

    crawler_dir: Path = Path(config.DATA_PATH).joinpath("crawler_data")
    parsed_dir = crawler_dir.parent.joinpath("parsed_data")
    parsed_dir.mkdir(parents=True, exist_ok=True)

    for file in parsed_dir.iterdir():
        file.unlink()

    bs4_transformer = BeautifulSoupTransformer()
    exclude = ["style", "script", "head", "title", "meta", "[document]", "a"]
    include = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "div", "span", "b", "i"]
    document = []
 
    for file in crawler_dir.iterdir():
        if file.is_dir():
            continue

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            doc =  Document(page_content=data, metadata={"source": "local"})
            document.append(doc)

    docs_transformed = bs4_transformer.transform_documents(document, unwanted_tags=exclude, tags_to_extract=include, remove_comments=True, remove_lines=False)

    for idx, file in enumerate(crawler_dir.iterdir()):
        if file.is_dir():
            continue
        
        with open(f"{parsed_dir.joinpath(file.with_suffix('.md').name)}", "w", encoding="utf-8", errors="ignore") as f:
            f.write(docs_transformed[idx].page_content)