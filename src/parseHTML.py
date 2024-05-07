import config
from pathlib import Path
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.docstore.document import Document
from bs4 import BeautifulSoup
from bs4.element import Comment


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



def parse_HTML_v2():
    """Parse the data collected by the crawler"""

    crawler_dir: Path = Path(config.DATA_PATH).joinpath("crawler_data")
    parsed_dir = crawler_dir.parent.joinpath("parsed_data_v2")
    parsed_dir.mkdir(parents=True, exist_ok=True)

    for file in parsed_dir.iterdir():
        file.unlink()

    document = []
 
    for file in crawler_dir.iterdir():
        if file.is_dir():
            continue

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            text = text_from_html(data)
            document.append(text)

    for idx, file in enumerate(crawler_dir.iterdir()):
        if file.is_dir():
            continue
        
        with open(f"{parsed_dir.joinpath(file.with_suffix('.md').name)}", "w", encoding="utf-8", errors="ignore") as f:
            f.write(document[idx])


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)