from typing import List
from sarthakai.genai.prompts import (
    SummarisationSystemPrompt,
    QueryRoutingSystemPrompt,
    TableDescriptionGenerationSystemPrompt,
)
from sarthakai.genai.llm import llm_call
from sarthakai.common import fuzzy_match_term_against_list_of_terms


def summarise_text(
    text_to_summarise: str, n_sentences: int, llm_name: str = "gpt-4o-mini"
):
    summarisation_system_prompt = SummarisationSystemPrompt(
        text_to_summarise=text_to_summarise, n_sentences=n_sentences
    )
    summarisation_messages = summarisation_system_prompt.messages
    summarised_text, cost = llm_call(messages=summarisation_messages, model=llm_name)
    return summarised_text


def describe_table(
    table_to_describe: str, n_sentences: int = 2, llm_name: str = "gpt-4o-mini"
):
    table_description_generation_system_prompt = TableDescriptionGenerationSystemPrompt(
        table_to_describe=table_to_describe, n_sentences=n_sentences
    )
    table_description_generation_messages = (
        table_description_generation_system_prompt.messages
    )
    table_description_text, cost = llm_call(
        messages=table_description_generation_messages, model=llm_name
    )
    return table_description_text


def route_query(query: str, routes: List[str], llm_name: str = "gpt-4o-mini"):
    query_routing_system_prompt = QueryRoutingSystemPrompt(query=query, routes=routes)
    query_routing_messages = query_routing_system_prompt.messages
    llm_predicted_route, cost = llm_call(
        messages=query_routing_messages, model=llm_name
    )

    fuzzy_matched_route = fuzzy_match_term_against_list_of_terms(
        term=llm_predicted_route, ground_truths=routes
    )
    return fuzzy_matched_route
