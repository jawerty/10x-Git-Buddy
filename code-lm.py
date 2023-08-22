import torch
from accelerate import Accelerator

class CoderLM:
  def __init__(self, model_name="bigcode/starcoder"):
    self.model_name = model_name
    self.load_8bit = True
    self.model = None;
    self.tokenizer = None;
    self.base_prompt = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request.

    ### Instruction:
    %s

    ### Response:
    """

  def load(self):
    self.model = AutoModelForCausalLM.from_pretrained(
        self.model_name,
        load_in_8bit=self.load_8bit,
        torch_dtype=torch.float16,
        device_map={"": Accelerator().process_index},
    )
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

  def get_api_prompt(self, description):
    return """
    You are given a GitHub issue description below. Using this description. Extract the classes, apis or methods that are mentioned in this GitHub issue.
    
    You must respond in the format below:
    APIS: your response goes here each item separated by commas
    
    The user's description is below:
    Description: %s
    """ % description

  def get_code_fixer_prompt(self, code, api, description):
    return """
    You are a bot that fixes code based on a user issue.
    
    You will be given the current source code of a file, the affected api class, variable or function, and the issue description. You must generate new source code updating the given source code based on the user's issue description.

    Here is the current source code below:
    CURRENTSOURCECODE: %s

    Here is the user's issue description below:
    USERDESCRIPTION: %s

    Here is the affected API below:
    API: %s

    You must respond with only the full fixed source code in markdown format after the keyword below:
    SOURCE CODE: write out the markdown code here

    You must only respond in the format I mentioned. Do not respond with any extra explanations except the source code for the fixed file in the format above.
    """ % (code, description, api)

  def get_code_relevance_prompt(self, code, description):
    return """
    You are a bot that determines whether source code is related to a GitHub issue description. You must only respond if it's relevant with "yes" or "no"
    
    You will be given the issue description and the source code. Be very discerning. If the file is not relevant, please say no. If it is relevant, sey yes.

    Here is the source code below:
    SOURCE CODE: %s

    Here is the description below:
    DESCRIPTION: %s

    You must only respond with either "yes" or "no" in the format below:
    RELVANCE: write yes or no here
    """ % (code, description)

  def get_instruction_prompt(self, instruction):
    return self.base_prompt % instruction

  def generate(self, instruction,
        input=None,
        temperature=1,
        top_p=0.9,
        top_k=40,
        num_beams=1,
        max_new_tokens=2048,
        **kwargs,):
    inputs = self.tokenizer(instruction, return_tensors="pt")
    input_ids = inputs["input_ids"].to("cuda")
    generation_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_beams=num_beams,
        eos_token_id=self.tokenizer.eos_token_id,
        pad_token_id=self.tokenizer.pad_token_id,
        **kwargs,
    )
    with torch.no_grad():
        generation_output = self.model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=max_new_tokens,
        )
    s = generation_output.sequences
    output = self.tokenizer.batch_decode(s, skip_special_tokens=True)
    return output
