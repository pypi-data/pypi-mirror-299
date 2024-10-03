import typing
import os
import time
from datetime import datetime
from typing import List, Dict, Set, Iterable
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from WPE.db import QdrantClientWrapper
from WPE.db.payloads import (
    PayloadContainer,
    WorkflowMappingPayloadContainer,
    WorkflowMappingTimeBasedClusterPayloadContainer,
)

# Utility function to convert points to payloads
def payloadsFromPoints(points, payload_type: PayloadContainer) -> typing.List[PayloadContainer]:
    """
    Converts a list of points into their respective payloads.

    Args:
        points: The raw data points retrieved from the database.
        payload_type: The specific payload container type to convert the points into.

    Returns:
        List of payloads extracted from the provided points.
    """
    wpe_payloads: typing.List[PayloadContainer] = []
    for p in points:
        wpe_payload = payload_type.fromPayload(p.payload)
        if wpe_payload is not None:
            wpe_payloads.append(wpe_payload)
    return wpe_payloads

# Class to represent individual events
class Event:
    def __init__(self, text: str, app_name: str, window_name: str, timestamp: datetime):
        """
        Initializes an Event instance.

        Args:
            text (str): The OCR text from the window.
            app_name (str): The name of the application.
            window_name (str): The name of the window.
            timestamp (datetime): The time when the event occurred.
        """
        self.text = text
        self.app_name = app_name
        self.window_name = window_name
        self.timestamp = timestamp

    def __repr__(self):
        return (f"Event(app_name='{self.app_name}', "
                f"window_name='{self.window_name}', "
                f"timestamp='{self.timestamp}')")

# Class to manage all events and fetch new ones from the database
class EventManager:
    def __init__(self):
        """
        Initializes the EventManager instance and loads events from the database.
        """
        self.events: List[Event] = []
        self.setup()

    def setup(self):
        """
        Fetches the events from the database and stores them in the manager.
        This function is called on initialization.
        """
        print('Fetching WPE events from Qdrant database...')
        qdrant_wrapper = QdrantClientWrapper()
        new_fetched_points = qdrant_wrapper.fetch(collection_name="jina")
        payloads = payloadsFromPoints(qdrant_wrapper.points, WorkflowMappingPayloadContainer)
        payloads = sorted(payloads, key=lambda x: x.timestamp, reverse=False)
        print(f'Total WPE events found in DB: {len(payloads)}')

        for p in payloads:
            # Convert timestamp from ms to seconds for better readability
            self.add_event(Event(p.ocrText, p.appTitle, p.windowTitle, p.timestamp / 1000.0))

    def add_event(self, event: Event):
        """
        Adds an event to the list of events.

        Args:
            event (Event): The event to be added.
        """
        self.events.append(event)

    # Event retrieval methods

    def get_events_by_app(self, app_name: str) -> List[Event]:
        """Returns a list of events filtered by the application name."""
        return [event for event in self.events if event.app_name == app_name]

    def get_events_by_window(self, window_name: str) -> List[Event]:
        """Returns a list of events filtered by the window name."""
        return [event for event in self.events if event.window_name == window_name]

    def get_events_by_app_and_window(self, app_name: str, window_name: str) -> List[Event]:
        """Returns events that match both the application and window names."""
        return [event for event in self.events if event.app_name == app_name and event.window_name == window_name]

    def get_all_window_names(self) -> List[str]:
        """Returns a list of all unique window names."""
        window_names = {event.window_name for event in self.events}
        return sorted(window_names)

    def get_all_app_names(self) -> List[str]:
        """Returns a list of all unique application names."""
        app_names = {event.app_name for event in self.events}
        return sorted(app_names)

    def get_windows_by_app(self, app_name: str) -> List[str]:
        """Returns all window names belonging to a specific application."""
        window_names = {event.window_name for event in self.events if event.app_name == app_name}
        return sorted(window_names)

    def get_all_apps_and_windows(self) -> Dict[str, Set[str]]:
        """
        Returns a dictionary with application names as keys and corresponding window names as values.
        """
        app_window_dict: Dict[str, Set[str]] = {}
        for event in self.events:
            app_window_dict.setdefault(event.app_name, set()).add(event.window_name)
        return app_window_dict

    def stringify_apps_and_windows(self) -> str:
        """
        Generates a formatted string representation of all applications and their windows.

        Returns:
            A string with the app names and their respective windows.
        """
        app_window_dict = self.get_all_apps_and_windows()
        result = ""
        for app, windows in app_window_dict.items():
            result += f"App: {app}\n"
            for window in windows:
                result += f"  Window: {window}\n"
        return result

# Class to handle cleaning OCR text using an LLM
class TextProcessor:
    def __init__(self, model_name: str = "gpt-4", api_key: str = None):
        """
        Initializes the TextProcessor for cleaning OCR text with a specified LLM.

        Args:
            model_name (str): The model name to be used (e.g., OpenAI model like 'gpt-4').
            api_key (str, optional): The API key for authentication with the LLM provider.
                                     Defaults to fetching from environment variables.
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set the api_key parameter or OPENAI_API_KEY environment variable.")

        # Initialize the OpenAI LLM with the provided model and API key
        self.llm = OpenAI(model_name=self.model_name, openai_api_key=self.api_key)

        # Define the prompt template for the LLM's input
        self.prompt_template = PromptTemplate(
            input_variables=["text"],
            template="""You are an AI assistant that cleans up OCR text by correcting errors, removing unwanted characters, and fixing formatting issues.

Original Text:
{text}

Cleaned Text:"""
        )
        # Create an LLM chain using the OpenAI model and the prompt template
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def touch_up_texts(self, texts: Iterable[str]) -> List[str]:
        """
        Processes an iterable of texts using the LLM to clean and correct them.

        Args:
            texts (Iterable[str]): A list or other iterable containing the texts to be cleaned.

        Returns:
            A list of cleaned texts.
        """
        cleaned_texts = []
        for text in texts:
            retry = True
            while retry:
                try:
                    # Process each text using the LLM chain
                    cleaned_text = self.chain.run(text=text)
                    cleaned_texts.append(cleaned_text.strip())
                    retry = False
                except Exception as e:
                    print(f"Error with LLM call: {e}. Retrying in 5 seconds...")
                    time.sleep(5)
        return cleaned_texts

# Class to select a subset of events based on length or importance (to be implemented)
class SubsetSelector:
    def __init__(self):
        """
        Initializes the SubsetSelector, used for selecting a subset of events based on certain criteria.
        """
        pass

    def select_subset(self, events: List[Event], max_length: int) -> List[Event]:
        """
        Selects a subset of events where the combined text length does not exceed max_length.
        Embedding models or other selection strategies could be used.

        Args:
            events (List[Event]): The list of events to select from.
            max_length (int): The maximum allowed text length for the selected subset.

        Returns:
            A list of selected events that meet the length constraint.
        """
        raise NotImplementedError
