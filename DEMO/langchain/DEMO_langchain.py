import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field

# Langchain imports
from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_core.output_parsers import PydanticOutputParser


class Country(BaseModel):
    capital: str = Field(description="capital of the country")
    population: int = Field(description="population of the country")
    name: str = Field (description="name of the country")

PROMPT_COUNTRY_INFO = """Provide information about {country}. If the country is not found make it up.
 {format_instructions}"""

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"

def main():
    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Country)

    # setup the chat model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)
    message = HumanMessagePromptTemplate.from_template(
        template=PROMPT_COUNTRY_INFO,
    )
    chat_prompt = ChatPromptTemplate.from_messages([message])

    # get user input
    country_name = input("Enter the name of a country: ")

    # generate the response
    print("Generating response...")
    chat_prompt_with_values = chat_prompt.format_prompt(
        country=country_name, format_instructions=parser.get_format_instructions()
    )
    output = llm(chat_prompt_with_values.to_messages())
    country = parser.parse(output.content)

    # print the response
    print(f"The capital of {country.name} is {country.capital} and the population is {country.population}.")


if __name__ == "__main__":
    main()