import openai as oai
import environ as env


# +++++++++ Parameters +++++++++++++++++++++++++
cwd = env.CURRENT_WORKING_DIR
# ++++++++++++++++++++++++++++++++++++++++++++++


# +++++++++  functions ++++++++++++++++++++++++++
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def ask_question(prompt, question):
    response = oai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role':'system', 'content':'You are a helpful assistant. The first prompt will be a long text,'
                                        'and any messages that you get be regarding that. Please answer any '
                                        'questions and requests having in mind the first prompt '},
            {'role':'user', 'content': prompt},
            {'role':'user', 'content': question}
        ]
    )
    return response.choices[0].message['content']
# ++++++++++++++++++++++++++++++++++++++++++++++++++


client = oai.OpenAI(api_key= env.OPENAI_API_KEY)
print()
print("OpenAI client registered.\n")
print()

content = read_file(env.GUB_FILE_INPUT_ADDR)
question = env.QUESTION

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
print(f"\n{response.output_text}", 
      file= str(env.GUB_OUTPUT_TXT_ADDR))


print(response.output[1].content[0].annotations)
print(response.output[1].content[0].annotations[0].url)


