from google import genai
import environ as env


# +++++++++ Parameters +++++++++++++++++++++++++
cwd = env.CURRENT_WORKING_DIR
# ++++++++++++++++++++++++++++++++++++++++++++++

# +++++++++  functions ++++++++++++++++++++++++++
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# ++++++++++++++++++++++++++++++++++++++++++++++++


client = genai.Client(api_key= env.GEMINI_API_KEY)
print()
print("Gemini client registered.\n")
print()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)



