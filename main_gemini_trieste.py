from google import genai
import environ as env

# +++++++++  functions ++++++++++++++++++++++++++
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# ++++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++ Parameters +++++++++++++++++++++++++
# cwd = env.CURRENT_WORKING_DIR
# content = read_file(env.TRIESTE_FILE_INPUT_ADDR)
# question = env.QUESTION_TRIESTE
# ++++++++++++++++++++++++++++++++++++++++++++++


client = genai.Client(api_key= env.GEMINI_API_KEY)
print()
print("Gemini client registered.\n")
print()

response = client.models.generate_content(
    model='gemini-3.1-pro-preview',
    contents= "What is AI?"
)
print(response.text)
print('\n=====================\n')

input_file = client.files.upload(file= env.TRIESTE_FILE_INPUT_ADDR)

response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[
        {"text": env.QUESTION_TRIESTE},
        input_file
    ]
)
print(response.text)

out_address = env.GEM_TRIESTE_OUTPUT_TXT_ADDR
with open(out_address, 'w') as out_file:
    out_file.write(response.text)

#print(response.output[1].content[0].annotations)
#print(response.output[1].content[0].annotations[0].url)


