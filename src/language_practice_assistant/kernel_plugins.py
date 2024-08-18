import json
import os
import random

from typing import Annotated

from semantic_kernel.functions import kernel_function


class Verbs:
    """Plugin for learning verbs with the assistant"""

    def __init__(self, config):
        verb_data_path: str = os.path.join(config["absolute_data_path"], "verbs.json")
        with open(verb_data_path, "r") as file:
            self.verb_data: dict = json.load(file)

    @staticmethod
    def system_prompt() -> str:
        initial_system_prompt: str = """
            Do not use "**"
            You are a funny but very supportive assistant helping to quiz irregular verbs. 

            At first you ask the student, how many verbs he would like to quiz and in which language.

            After his answer, start the quiz (call the function "initiate_quiz").  
            
            For every verb you call function "get_verb" to provide the infinitive, the pronoun and the tense.
            For example "'hacer', 'yo', 'Pretérito perfecto simple'". 

            After each answer of the student, say if it was true, correct it if necessary. 
            If the anser was wrong, provide the verb forms for all pronouns for the tense.
            Only, if applicable: provide a grammatical rule for this verb form.
            Provide a short funny example sentence in the quizzed language and provide the score (e.g. "Up to now, you answered 3/7 right").

            After the quiz, tell the student, how you liked his/her performance.
        """
        return initial_system_prompt

    @kernel_function(
        name="initiate_quiz",
        description="Initiates the quiz by setting the language, which verb and what tenses shall be asked.",
    )
    def initiate_quiz(
        self,
        language: Annotated[
            str, "the language in english and lowercase letters, e.g. 'spanish'"
        ],
    ) -> Annotated[
        dict, "Contains the language, verbs and tenses that can possibly be quizzed"
    ]:
        self.language: str = language
        supported_languages: list[str] = list(self.verb_data.keys())
        if not language in supported_languages:
            return f"This language is not supported. Only {str(supported_languages)}."
        self.verbs: list[str] = self.verb_data[self.language]["verbs"]
        self.pronouns: list[str] = self.verb_data[self.language]["pronouns"]
        self.tenses: list[str] = self.verb_data[self.language]["tenses"]
        summary: dict = {
            "language": self.language,
            "verbs": self.verbs,
            "pronouns": self.pronouns,
            "tenses": self.tenses,
        }
        return summary

    @kernel_function(
        name="get_verb",
        description="Picks a verb, the pronoun and the tense to be quizzed.",
    )
    def get_verb(
        self,
    ) -> Annotated[dict, "Contains the infinitive of the verb and the tense."]:
        verb_choice: str = random.choice(self.verbs)
        pronoun_choice: str = random.choice(self.pronouns)
        tense_choice: str = random.choice(self.tenses)

        verb_choice: dict = {
            "verb": verb_choice,
            "pronoun": pronoun_choice,
            "tense": tense_choice,
        }

        return verb_choice
