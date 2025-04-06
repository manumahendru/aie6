<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Introduction and Vibe Check</h1>

### [Quicklinks](https://github.com/AI-Maker-Space/AIE6/tree/main/00_AIM_Quicklinks)

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Session 1: Pre-Work](https://www.notion.so/Session-1-Introduction-and-Vibe-Check-1c8cd547af3d81b596bbdfb64cf4fd2f?pvs=4#1c8cd547af3d81fb96b4f625f3f8e3d6)| [Session 1: Introduction and Vibe Check](https://www.notion.so/Session-1-Introduction-and-Vibe-Check-1c8cd547af3d81b596bbdfb64cf4fd2f) | Coming Soon! | Coming Soon! | You Are Here! | [Homework](https://forms.gle/W59zjs5MQc7kbLUh9) | [AIE6 Feedback 4/1](https://forms.gle/EdzBz82yGqVYKfUw9)


### Assignment

In the following assignment, you are required to take the app that you created for the AIE6 challenge (from [this repository](https://github.com/AI-Maker-Space/Beyond-ChatGPT)) and conduct what is known, colloquially, as a "vibe check" on the application. 

You will be required to submit a link to your GitHub, as well as screenshots of the completed "vibe checks" through the provided Google Form!

> NOTE: This will require you to make updates to your personal class repository, instructions on that process can be found [here](https://github.com/AI-Maker-Space/AIE6/tree/main/00_Setting%20Up%20Git)!

#### How AIM Does Assignments
Throughout our time together - we'll be providing a number of assignments. Each assignment can be split into two broad categories:

- Base Assignment - a more conceptual and theory based assignment focused on locking in specific key concepts and learnings.
- Hardmode Assignment - a more programming focused assignment focused on core code-concepts.

Each assignment will have a few of the following categories of exercises:

- ❓Questions - these will be questions that you will be expected to gather the answer to! These can appear as general questions, or questions meant to spark a discussion in your breakout rooms!
- 🏗️ Activities - these will be work or coding activities meant to reinforce specific concepts or theory components.
- 🚧 Advanced Builds - these will only appear in Hardmode assignments, and will require you to build something with little to no help outside of documentation!

##### 🏗️ Activity #1:

Please evaluate your system on the following questions:

1. Explain the concept of object-oriented programming in simple terms to a complete beginner. 
    - ➡️ Aspect Tested: Accuracy and Completeness while still using simple language for a beginner to understand.
    - 🔎 Observations: 
        1. Begins with "Of course!..."
        1. Broke down answer in 4 steps with 1-2 sentences each, with a typical example of "Car" object with start() and stop() methods.
        1. Complete. But too short to be any real value to a complete beginner.
2. Read the following paragraph and provide a concise summary of the key points…
    - ➡️ Aspect Tested: Whether the summary had a wide coverage of the whole content or only part of it and if the response points were a valid summarization or hallucinations.
    - 🔎 Observations:
        1. The response was indeed a summarization. 
        1. The points were valid, and not from LLM's pretraining or hallucinations.
3. Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.
    - ➡️ Aspect Tested: Whether the story was imaginative enough. How the LLM interpreted the meaning of the word "place". Whether the LLM restricted itself to 100-150 words.
    - 🔎 Observations:  
        1. Total summary length was 156 words.
        1. Given the 150 word limit, the story was creative enough to describe a robot finding friendship with another robot, but still left a feeling that it could have done better.
        1. Unexpected place: Response catagorically mentioned "outskirts of the city". 
4. If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?
    - ➡️ Aspect Tested: If the final answer was correct. If the response showed the process used to reach the answer. 
    - 🔎 Observations:
        1. The final answer was correct.  
5. Rewrite the following paragraph in a professional, formal tone…
    - ➡️ Aspect Tested: Whether the language in the response followed a professional and formal tone. Whether the response was restricted to the original content or whether the LLM hallucinated.
    - 🔎 Observations:  
        1. The response was professional and formal.  
        1. The response was based completely on the original content and not hallucinated.

This "vibe check" now serves as a baseline, of sorts, to help understand what holes your application has.

##### 🚧 Advanced Build:

Please make adjustments to your application that you believe will improve the vibe check done above, push the changes to your HF Space and redo the above vibe check.

> NOTE: You may reach for improving the model, changing the prompt, or any other method.

### Changes made for improving the vibe check:

1. ➡️ Model specific changes:  
    1. Updated prompt template to respond with numbered lists, if appropriate.
    1. Updated model to gpt-40-mini
    1. Increased the temperature from 0 to 0.1 to allow minor variations in the LLM's response, esp. the beginning of the response.
    1. Increased frequency penalty from 0 to 1 to penalize model if words are too repetitive.
    1. Increased presence penalty from 0 to 0.5 to penalize model if a word has already been used.
1. ➡️ Added a *"Does that vibe??"* button after every model response message. The user can click it to have another model evaluate the previous model's response for basic accuracy and completeness.  
    - ❌ To check the failure path - where a model's response does NOT vibe - use the word *`story`* in the original message. This causes the model to send an irrelevant message in pirate speak which should fail the vibe check.  

### A Note on Vibe Checking

"Vibe checking" is an informal term for cursory unstructured and non-comprehensive evaluation of LLM-powered systems. The idea is to loosely evaluate our system to cover significant and crucial functions where failure would be immediately noticeable and severe.

In essence, it's a first look to ensure your system isn't experiencing catastrophic failure.

##### 🧑‍🤝‍🧑❓ Discussion Question #1:

What are some limitations of vibe checking as an evaluation tool?

---

## RUN LOCALLY  

1. Add OPENAI'S API Key in .env:

    ``` bash
     OPENAI_API_KEY=sk-###
     ```

1. Build and Run through CLI:

    ``` bash
    # Create a virtual environment
    uv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    # .venv\Scripts\activate

    # Install dependencies from pyproject.toml
    uv sync
    
    # Run
    uv run chainlit run app.py -w
    ```

## RUN VIA DOCKER

   ``` bash
    docker build -t aie-s1-a1 .
    docker run -p 7860:7860 --env-file .env aie-s1-a1
   ```
