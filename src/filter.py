import config
from pathlib import Path
from gpt import init_agent

def use_gpt(data: str, organization: str) -> str:
    """Use the GPT model to filter the data"""
    agent = init_agent()

    response = agent.invoke(f"""You are an investigator looking for information about a company and it's employees.
                            This includes, but is not limited to, contact information, organization number, products, services,
                            and other information that would help give a more complete picture of the company.
                            You are specifically looking for information about the the company called {organization}.
                            Only respond with relevant information. if absolutely no useful information can be extract from the text,
                            respond with 'NOTHING'. If specific information is not present in the text, do not make up information,
                            instead designate the information as 'not found'.
                            Can you efficiently extract the relevant information from the following text:\n
                            {data}""")
    
    return response.content if "NOTHING" not in response.content else ""


def filter_data(organization: str) -> None:
    """Filter parsed data extract relevant information"""
    parsed_dir: Path = Path(config.DATA_PATH).joinpath("parsed_data")
    filtered_dir = parsed_dir.parent.joinpath("filtered_data")
    filtered_dir.mkdir(parents=True, exist_ok=True)
    for file in filtered_dir.iterdir():
        file.unlink()

    for file in parsed_dir.iterdir():
        result = ""
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = ""
            tokens = 0
            # read at least 3000 tokens before invoking the model (model limit of gpt-35 is 4096 tokens)
            while True:
                new_line = f.readline()
                if len(new_line) == 0:
                    # end of file
                    gpt_response = use_gpt(data, organization)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    break
                elif tokens > 3000:
                    # approaching token limit
                    data += new_line
                    gpt_response = use_gpt(data, organization)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    data = ""
                    tokens = 0
                else:
                    # continue reading
                    data += new_line
                    tokens += len(new_line.split())

        # write the filtered data to a new file
        if len(result) > 0:
            with open(f"{filtered_dir.joinpath(file.name)}", "w", encoding="utf-8", errors="ignore") as f:
                f.write(result)


def remove_duplicates() -> None:
    """Remove duplicate information from the filtered data"""
    filtered_dir: Path = Path(config.DATA_PATH).joinpath("filtered_data")

    for file in filtered_dir.iterdir():
        duplicate_free = ""
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            # remove duplicates
            agent = init_agent()
            response = agent.invoke(f"""return the same exact information back to me after removing duplicate information within the data:\n
                                    {data}""")
            duplicate_free = response.content
        with open(f"{filtered_dir.joinpath(file.name)}", "w", encoding="utf-8", errors="ignore") as f:
            f.write(duplicate_free)