def get_prompt(prompt_name):
    file_path = f"api/openAI/prompts/{prompt_name}.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read and return the content of the file
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    except IOError as e:
        raise IOError(f"An error occurred while reading the file '{file_path}': {e}")
