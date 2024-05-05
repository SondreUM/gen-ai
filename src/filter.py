import config
from pathlib import Path
from gpt import init_agent
import os
from openai import BadRequestError

def use_gpt(data: str, organization: str, file: Path) -> str:
    """Use the GPT model to filter the data"""
    agent = init_agent()

    prompt = f"""You are an investigator looking for information about a company and it's employees.
            This includes, but is not limited to, contact information, organization number, products, services,
            and other information that would help give a more complete picture of the company.
            You are specifically looking for information about the the company called {organization}.
            Only respond with relevant information. if absolutely no useful information can be extract from the text,
            respond with 'NOTHING'. If specific information is not present in the text, do not make up information,
            instead designate the information as 'not found'.
            Can you efficiently extract the relevant information from the following text:\n
            {data}"""

    try:
        max_tokens = 4096 if 16385 - len(prompt) > 4096 else 16385 - len(prompt)
        response = agent.invoke(prompt, max_tokens=max_tokens)
    except ValueError as e:
        # Handle error thrown by Azure content filter
        print(f"failed to filter part of {file.name} due to error: {e}")
        print(f"saving data to file for manual review")
        review_dir = Path(config.DATA_PATH).joinpath("review_data")
        with open(review_dir.joinpath(file.name), "a", encoding="utf-8", errors="ignore") as f:
            f.write(data)
        return ""
    except BadRequestError as e:
        # print debug info in case LLM is unhappy with prompt
        print(e)
        print(f"prompt: {len(prompt)}")
        print(prompt)

        exit()

    ret = "" if "NOTHING" in response.content else response.content
    return ret


def filter_data(organization: str) -> None:
    """Filter parsed data extract relevant information"""
    parsed_dir: Path = Path(config.DATA_PATH).joinpath("parsed_data")
    filtered_dir = parsed_dir.parent.joinpath("filtered_data")
    filtered_dir.mkdir(parents=True, exist_ok=True)
    review_dir = Path(config.DATA_PATH).joinpath("review_data")
    review_dir.mkdir(parents=True, exist_ok=True)
    for file in filtered_dir.iterdir():
        file.unlink()
    for file in review_dir.iterdir():
        file.unlink()

    for file in parsed_dir.iterdir():
        result = ""
        print(f"filtering {file}")
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = ""
            tokens = 0
            # read at least 3000 tokens before invoking the model (model limit of gpt-35 is 4096 tokens / 16385 characters)
            while True:
                new_line = f.readline()
                if len(new_line) // 4 + tokens > 3500:
                    # handle excessively large lines
                    to_read = 3500 - tokens
                    tokens = 0
                    data += new_line[:to_read]
                    new_line = new_line[to_read:]
                    gpt_response = use_gpt(data, organization, file)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    while len(new_line) > 0:
                        to_read = len(new_line) if len(new_line) // 4 < 3000 else 3000*4
                        data = new_line[:to_read]
                        new_line = new_line[to_read:]
                        gpt_response = use_gpt(data, organization, file)
                        if len(gpt_response) > 0:
                            result += f"\n{gpt_response}"
                if len(new_line) == 0:
                    # end of file
                    gpt_response = use_gpt(data, organization, file)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    break
                elif tokens > 3000:
                    # approaching token limit
                    data += new_line
                    gpt_response = use_gpt(data, organization, file)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    data = ""
                    tokens = 0
                else:
                    # continue reading
                    data += new_line
                    tokens += len(new_line) // 4

        # write the filtered data to a new file
        if len(result) > 0:
            with open(f"{filtered_dir.joinpath(file.name)}", "w", encoding="utf-8", errors="ignore") as f:
                f.write(result)

    generate_report()


def generate_report() -> None:
    """Remove duplicate information from the filtered data"""
    print("Generating report")
    filtered_dir: Path = Path(config.DATA_PATH).joinpath("filtered_data")
    report_file = filtered_dir.parent.joinpath("report.md")

    files = os.listdir(filtered_dir)
    with open(filtered_dir.joinpath(files[0]), "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
        with open(report_file, "w", encoding="utf-8", errors="ignore") as f:
            f.write(data)

    for i in range(1, len(files)):
        duplicate_free = ""
        with open(filtered_dir.joinpath(files[i]), "r", encoding="utf-8", errors="ignore") as f:
            with open(report_file, "r", encoding="utf-8", errors="ignore") as rf:
                data = rf.read() + "\n" + f.read()
                # remove duplicate information
                agent = init_agent()
                response = agent.invoke(f"""return the same exact information back to me after removing duplicate information within the data:\n
                                        {data}""")
                duplicate_free += response.content

        with open(report_file, "w", encoding="utf-8", errors="ignore") as f:
            f.write(duplicate_free)
