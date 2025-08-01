from visbox.datatypes import LabelResult, AutoLabelFormat


def gen_result_from_output(input: AutoLabelFormat, output: str) -> LabelResult:
    try:
        return {
            "id": input["id"],
            "data": input,
            "explanation": output,
            "category": output.split('```')[1].strip()
            }
    except:
        return {
            "id": input["id"],
            "data": input,
            "explanation": output,
            "category": None
            }
