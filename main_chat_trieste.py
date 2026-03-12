import openai as oai
import environ as env


# +++++++++ Parameters +++++++++++++++++++++++++
cwd = env.CURRENT_WORKING_DIR
# ++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++  functions ++++++++++++++++++++++++++
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++


client = oai.OpenAI(api_key= env.OPENAI_API_KEY)
print()
print("OpenAI client registered.\n")
print()

content = read_file(env.TRIESTE_FILE_INPUT_ADDR)
question = env.QUESTION_TRIESTE

response = client.responses.create(
        model= "gpt-5",
        reasoning= {"effort": "medium"},
        tools= [
            {
                "type": "web_search",
                "user_location": {
                    "type": "approximate",
                    "country": "US"
                }
            }
        ],
        tool_choice= "auto",
        include= ["web_search_call.action.sources"],
        input= [
            {
                "role": "developer",
                "content": content,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

print(f"\n{response.output_text}")

out_address = env.TRIESTE_OUTPUT_TXT_ADDR
with open(out_address, 'w') as out_file:
    out_file.write(response.output_text)

#print(response.output[1].content[0].annotations)
#print(response.output[1].content[0].annotations[0].url)


