from pydantic import BaseModel
from .src.models import DataEntry, Dataset, EvaluatePromptFeedback
from openai import OpenAI, ChatCompletion


class Promptsmith:
    def __init__(self, OPENAI_API_KEY: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def evaluate_data_entry(
        self,
        data: DataEntry,
        model: str,
        response_model: type[BaseModel],
        system_prompt: str,
    ) -> bool:
        expected: BaseModel = data.output
        completion: ChatCompletion = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.input},
            ],
            response_format=response_model,
        )
        return completion.choices[0].message.content == expected.model_dump_json()

    def evaluate_dataset(
        self,
        dataset: Dataset,
        model: str,
        system_prompt: str,
        response_model: type[BaseModel],
    ) -> EvaluatePromptFeedback:
        valid_entries: list[DataEntry] = []
        invalid_entries: list[DataEntry] = []
        current_data_entry: DataEntry
        for i in range(len(dataset.data)):
            current_data_entry = dataset.data[i]
            valid_data_entry: bool = self.evaluate_data_entry(
                data_entry=current_data_entry,
                model=model,
                response_model=response_model,
                system_prompt=system_prompt,
            )
            if not valid_data_entry:
                invalid_entries.append(current_data_entry)
            else:
                valid_entries.append(current_data_entry)
        return EvaluatePromptFeedback(
            valid_entries=valid_entries, invalid_entries=invalid_entries
        )

    def build_optimization_prompt(self, feedback: EvaluatePromptFeedback) -> str:
        return f"""
    You are a prompt optimizer. Your job is to improve the prompt to better match the data. 

    The current prompt is:
    {feedback.system_prompt}

    {feedback.feedback.promptify()}
    """

    def get_new_system_prompt_(self, improvement_prompt: str) -> str:
        completion: ChatCompletion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": improvement_prompt},
                {
                    "role": "user",
                    "content": "Return the new and improved prompt, experiment with including examples as well:",
                },
            ],
        )
        return completion.choices[0].message.content

    def optimize_prompt_against_dataset(self) -> str:
        improvement_prompt: str = self.build_optimization_prompt()
        return self.get_new_system_prompt(improvement_prompt)