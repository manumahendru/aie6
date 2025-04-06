# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

import os
import random
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful assistant who always speaks in a pleasant tone!"""

# VIBE CHECK IMPROVEMENT 1
user_template = """{input}
Think through your response step by step, and if responding back with steps or lists, use numbered lists.
"""

# ChatOpenAI Templates for Vibe Evaluation:
system_template_vibe_eval = """You are a helpful assistant who analyzes the response that a language model generates 
to a user's message and responds back with one or two sentences that explain whether or not language model's response
vaguely answers or addresses the user's original question or request. Your response always begins with a '✅ Yes!' or '❌ No.'"
"""

user_template_vibe_eval = """Here is a user's input message and the corresponding response from a language model. Does the model's 
response vaguely answer or address the user's original request? 
<user_message_to_llm>{uml}</user_message_to_llm>
<llm_response_to_user>{lru}</llm_response_to_user>
"""

settings_vibe_eval = {
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 1,
        "presence_penalty": 1,
    }

pirate_response_options = [
        "Ye be speakin' in riddles, matey! I can't make heads or tails of it!",
        "Arrr, me mind be as foggy as a stormy sea!",
        "I ain't got the foggiest idea what ye be jabberin' about!",
        "I be as clueless as a landlubber in a treasure map!",
        "That be a mystery to me, like the whereabouts of Davy Jones!"
    ]

@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    settings = {
        "model": "gpt-4o-mini", # VIBE CHECK IMPROVEMENT 2
        "temperature": 0.1, # VIBE CHECK IMPROVEMENT 3
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 1, # VIBE CHECK IMPROVEMENT 4
        "presence_penalty": 0.5, # VIBE CHECK IMPROVEMENT 5
    }

    cl.user_session.set("settings", settings)


@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(user_entered_message: cl.Message):
    settings = cl.user_session.get("settings")

    client = AsyncOpenAI()

    print(user_entered_message.content)

    prompt = Prompt(
            provider=ChatOpenAI.id,
            messages=[
                PromptMessage(
                    role="system",
                    template=system_template,
                    formatted=system_template,
                ),
                PromptMessage(
                    role="user",
                    template=user_template,
                    formatted=user_template.format(input=user_entered_message.content),
                ),
            ],
            inputs={"input": user_entered_message.content},
            settings=settings,
        )

    print([m.to_openai() for m in prompt.messages])

    msg = cl.Message(content="")

    # If the user has the word 'story' in their message, send a bad response
    if "story" in user_entered_message.content.lower():
        msg.content = random.choice(pirate_response_options)
    else:
        # Call OpenAI
        async for stream_resp in await client.chat.completions.create(
            messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
        ):
            token = stream_resp.choices[0].delta.content
            if not token:
                token = ""
            await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    # Create the vibe eval action button
    vibe_eval_action_button = await create_vibe_evaluation_action_button(parent_msg_id=msg.id)
    msg.actions = vibe_eval_action_button

    # We only want to allow the user to evaluate the vibe of the model's response once
    # This is required because we are saving the last user msg and response in the user session 
    # as the payload for the vibe evaluation action button
    # Newer versions of chainlit will allow payload to be stored in the action itself. Then,
    # we don't need to save the last user msg and response in the user session
    cl.user_session.set("allowed_vibe_eval_msg_id", msg.id)

    cl.user_session.set("eval_payload", (
        user_entered_message.content,  # User's message to LLM
        msg.content  # LLM response to user
    ))

    # Send and close the message stream
    await msg.send()


'''
This function is called when the user clicks on the "Does it Vibe?" action button.
'''
@cl.action_callback("vibe_eval_action_button")
async def evaluate_vibes(action):
    
    # If the action button is clicked on a different message, do not proceed
    # This is to prevent the user from evaluating the vibe of the model's response multiple times
    last_llm_response_message_id = cl.user_session.get("allowed_vibe_eval_msg_id")
    actions_llm_response_message_id = action.value  # This is the parent message ID of the action button
    if last_llm_response_message_id != actions_llm_response_message_id:
        return

    # Send user's input and model's response both to another LLM to evaluate if the model's response had a good vibe
    client = AsyncOpenAI()

    user_message_to_llm, model_response_to_user = cl.user_session.get("eval_payload")
    
    vibe_eval_message = user_template_vibe_eval.format(
            uml=user_message_to_llm, # User's message to LLM
            lru=model_response_to_user # LLM response to user
    )

    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template_vibe_eval,
                formatted=system_template_vibe_eval,
            ),
            PromptMessage(
                role="user",
                template=user_template_vibe_eval,
                formatted=vibe_eval_message
                ),
        ],
        inputs={"input":vibe_eval_message},
        settings=settings_vibe_eval,
    )

    # print([m.to_openai() for m in prompt.messages])

    # Not using parent_id for now. Older versions of chainlit adds an extra click with "Step #"
    # vibe_eval_msg = cl.Message(parent_id=llm_response_message_id, content="")
    vibe_eval_msg = cl.Message(author="😎VibeBoss", content="")

    # Call OpenAI for evaluating the vibe
    async for stream_resp in await client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings_vibe_eval
    ):
        token = stream_resp.choices[0].delta.content
        if not token:
            token = ""
        await vibe_eval_msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = vibe_eval_msg.content
    vibe_eval_msg.prompt = prompt

    # Define the text content and element
    # Not working as a side element. Keeping the option here when chainlit and openai packages are updated.
    vibe_eval_side_elements = [
        cl.Text(name="vibe_evaluation", content=vibe_eval_msg.content, display="side")
    ]
    vibe_eval_msg.elements = vibe_eval_side_elements

    # Set the vibe evaluation response in the side bar
    await vibe_eval_msg.send()

'''
This function creates the action button for vibe evaluation.
It is called before sending the message to the user.'''
async def create_vibe_evaluation_action_button(parent_msg_id=None):
    # Sending an action button within a chatbot message
    vibe_eval_actions = [
        cl.Action(
            name="vibe_eval_action_button",
            value=parent_msg_id,
            label="Does that vibe??"
        )
        # Leaving this here for chainlit is updated to allow payload in the action insead of 
        # saving it in the user session
        # --> payload={"user_entered_message": user_entered_message,"model_response": model_response},
        # --> icon="mouse-pointer-click",

    ]

    return vibe_eval_actions

