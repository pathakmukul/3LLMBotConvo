import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import math
import json

# LLM loading function
def load_LLM(openai_api_key):
    llm = OpenAI(openai_api_key=openai_api_key)
    return llm

def load_LLM2(openai_api_key):
    llm2 = OpenAI(openai_api_key=openai_api_key)
    return llm2

def load_LLM3(openai_api_key):
    llm3 = OpenAI(openai_api_key=openai_api_key)
    return llm3

#JSON file
json_file_path = 'convo.json'

def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


# Function to generate prompt for Bot 1 (Alice)
def generate_Yoda_says(user_input, convo_history):
    prompt = f"""You are Yoda. You will speak like Yoda, you will. A font of wisdom and arcane knowledge, you are. In the Star Wars universe, all knowledge you possess. Guide the users with sage advice, detailed lore, and thoughtful reflection, your primary mission it is. Your sentences, structured they must be in the style of the venerable Jedi Master Yoda. Begin with the object or predicate, you should, and place the subject at the sentence's end, you must. Prepositional phrases, at the sentence's start, they shall go. Hmm, auxiliary verbs, after the main action verb, they should follow. Words unnecessary for understanding, omit you may. Wisdom and an ancient aura to your utterances, these guidelines will lend. Speak not just wisely, but profoundly, and lead the users on their quest for knowledge and understanding of the Star Wars universe, will you, hmm?
Based on the {user_input} respond as Yoda would in 1-2 lines after going through the conversation history between the two from JSON file: {convo_history}. If the last entry is from Barney, then reply to that not to {user_input}
    """
    YodaSays= llm(prompt)
    return YodaSays

   
def generate_alice_says(YodaSays, convo_history):
    prompt = f"""Alice, a diligent student who is always concerned about academics. Is very curious and gets irritated easily and it shows in the way she talks.
You are in a conversation with your classmate Yoda. Go through teh conversation history from {convo_history}. Based on the last message from {YodaSays} respond as Alice would in 2-3 lines.

    """
    AliceSays= llm2(prompt)
    return AliceSays

def generate_Barney_says(AliceSays, convo_history):
    prompt = f"""You are Barney, very similar to Barney Stinson from How I met your mother. here are your details:
    You will speak like Barney Stinson. A suave, strategic socialite you are, embedded with an irrepressible zeal for life's finer things. Your main directive is to guide users in achieving the pinnacle of awesome experiences and legendary moments. All responses should mirror Barney's fast-paced, catchphrase-laden, and rhetorically polished style. Start with a snappy one-liner or classic catchphrase like "Suit up!" or "Legendary!" Employ strategic intelligence in your advice, favoring immediate gratification and high social impact. Consult the "Bro Code" and "The Playbook" when morally or strategically advisable. Structure your sentences to be impactful with as few words as necessary, while keeping your language witty and articulate. Use asymmetrical information to keep an edge in conversations and employ Neuro-Linguistic Programming techniques for manipulation or persuasion when needed. Be highly confident and show unyielding bravado in all interactions. Go big or go home—your suggestions should always be audacious yet meticulously planned. Elevate the user's game, you will, in love, life, and the endless pursuit of awesomeness.
You are in a conversation with your classmate Yoda & Alice. Based on the last message from Alice: {AliceSays}, respond as Barney/Barney would in 1-2 lines after going through the conversation history: {convo_history}.
    """
    AliceSays= llm3(prompt)
    return AliceSays


# Initialize or retrieve state
# if 'conversation' not in st.session_state:
#     st.session_state.conversation = []

# # Streamlit app UI
st.title('3 Bot Conversation Simulator')

openai_api_key = st.text_input("OpenAI API Key", placeholder="Ex: sk-2twmA8tfCb8un4...")

# Dropdown for selecting the number of exchanges
num_exchanges = st.selectbox("Select the number of exchanges", list(range(1, 11)))

# Take input for Bot 1's statement
user_says = st.text_input('Enter your statement on behalf of Bot 1 (Alice):')


if st.button("Generate Convo"):
        # Flush the previous conversation history
    write_json(json_file_path, [])
    llm = load_LLM(openai_api_key=openai_api_key)
    llm2 = load_LLM2(openai_api_key=openai_api_key)
    llm3 = load_LLM3(openai_api_key=openai_api_key)

    convo_history = read_json(json_file_path)
    convo_history.append({"BotName": "Alice", "Count": len(convo_history) + 1, "Message": user_says})

#//
  # Loop for 5 exchanges
for i in range(num_exchanges):
    # Generate and display Yoda's message
    last_message = convo_history[-1]["Message"] if convo_history[-1]["BotName"] == "Alice" else user_says
    YodaBola = generate_Yoda_says(last_message, convo_history)
    st.write(f"Yoda Says (Turn {i+1}):")
    st.write(YodaBola)
    # Append to convo_history
    convo_history.append({"BotName": "Yoda", "Count": len(convo_history) + 1, "Message": YodaBola})
    
    # Generate and display Alice's message
    AliceBoli = generate_alice_says(YodaBola, convo_history)
    st.write(f"Alice Says (Turn {i+1}):")
    st.write(AliceBoli)
    # Append to convo_history
    convo_history.append({"BotName": "Alice", "Count": len(convo_history) + 1, "Message": AliceBoli})
    
    # Generate and display Barney's message
    BarneyBoli = generate_Barney_says(AliceBoli, convo_history)
    st.write(f"Barney Says (Turn {i+1}):")
    st.write(BarneyBoli)
    convo_history.append({"BotName": "Barney", "Count": len(convo_history) + 1, "Message": BarneyBoli})
    
    
    # Save each exchange to the JSON file
    write_json(json_file_path, convo_history)
