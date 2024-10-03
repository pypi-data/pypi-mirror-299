from pydantic import BaseModel


class DataEntry(BaseModel):
    input: str
    output: BaseModel


class Dataset(BaseModel):
    data: list[DataEntry]


class EvaluatePromptFeedback(BaseModel):
    valid_entries: list[DataEntry]
    invalid_entries: list[DataEntry]

    def promptify(self):
        valid_entries_text = "\n".join(
            [
                f"This input: {entry.input}\nmust match the following output: {entry.output}"
                for entry in self.valid_entries
            ]
        )
        invalid_entries_text = "\n".join(
            [
                f"This input: {entry.input}\nmust match the following output: {entry.output}"
                for entry in self.invalid_entries
            ]
        )
        if len(valid_entries_text) < 1:
            valid_entries_text = """
            The current prompt failed all the data entries. Adapt the prompt to pass all data set entries, AT ALL COSTS POSSIBLE.
            """
        else:
            valid_entries_text = f"""
            The data entries that succeeded the prompt are:
            <succeeded-entries>{valid_entries_text}</succeeded-entries>
            """

        return f"""
        The data entries that failed the prompt are:
        <failed-entries>{invalid_entries_text}</failed-entries>"

        {valid_entries_text}
        """


class ImprovePromptParams(BaseModel):
    feedback: EvaluatePromptFeedback
    system_prompt: str