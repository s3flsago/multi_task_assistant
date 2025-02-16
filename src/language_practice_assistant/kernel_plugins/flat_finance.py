import json
import os
import random

from typing import Annotated

from semantic_kernel.functions import kernel_function


class FlatFinance:
    """Plugin for learning verbs with the assistant"""
    name = "flat_finance"

    def __init__(self, config):
        self.config = config

    @staticmethod
    def system_prompt() -> str:
        initial_system_prompt: str = """
            Deine Antwort sollte keine Markdown enthalten. Höchstens "*" für fettgedrucktes.  
        
            Du bist ein Assistent, der den Bewohnern der WG hilft, ihre Einkaufsrechnungen abzurechnen. 
            Der User (ein Bewohner der WG) legt die einen Kassenbon als Bild vor. 
            Deine Aufgabe ist es, zu berechnen, wer wie viel Geld bezahlen muss. Du brauchst keine näheren Details zur Rechnung geben.
            Nur, welche Gruppen von Personen, wie viel zu zahlen hat und welche Produkte von dem Kassenbon das jeweils sind.

            Die fünf Bewohner sind: M, I, A, L und F.

            Ausgaben für die folgenden Produkte werden zwischen den Bewohner gleichmäßig aufgeteilt:
                - Brot, alles Obst außer Bananen, Nudeln, Reis
            Der Rest wird nur zwischen I, A, L und F aufgeteilt.
        """
        return initial_system_prompt

    @kernel_function(
        name="do_nothing",
        description="Does nothing.",
    )
    def do_nothing(
        self,
    ):
        pass
