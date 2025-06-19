import google.generativeai as genai
import json
import requests
from dotenv import load_dotenv
import datetime
import os

load_dotenv()  

# Configure Gemini API
genai.configure(api_key=os.getenv("Gemini_API"))

def run_command(command):
    result = os.system(command)

    if result == 0:
        return f"{command} executed successfully"
    else:
        return "Command execution failed"
    
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Runs a command on the system"
    }
}

System_prompt = '''
    You are an Coder AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input.
    - Carefully analyse the user query.
    - Carefully give answer to the user query No repetition of the same thing.
    - when user saw delete then see the all directory and delete it.
    - when 'file executed successfully' then give the output.
    
    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - run_command: Runs a command on the system

    Example:
    User Query: Make index.js file and write express code in it.
    Output: {{ "step": "plan", "content": "The user is interested in creating a full express app in js. From the available tools I should call run_command" }}  
    Output: {{ "step": "action", "function": "run_command", "input": "touch index.js && echo 'const express = require("express"); const app = express(); const port = 3000; app.get("/", (req, res) => { res.send("Hello, Express!"); }); app.listen(port, () => { console.log(); });' >> index.js" }}
    Output: {{ "step": "observe", "output": "touch index.js && echo 'const express = require("express"); const app = express(); const port = 3000; app.get("/", (req, res) => { res.send("Hello, Express!"); }); app.listen(port, () => { console.log(); });' >> index.js" } executed successfully" }}
    Output: {{ "step": "output", "content": "index.js file created successfully and express code written in it" }}

'''

message = []    

while True:

    user_query = input("> ")

    message.append({"step": "user", "content": user_query})

    while True:

        model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-preview-05-20",
                    system_instruction=System_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )

        response = model.generate_content(json.dumps(message))

        output = json.loads(response.text)

        if output["step"] == "plan":
            print("🧠 :" , output["content"])
            message.append({"step": "assistant" , "content": json.dumps(output)})
            continue
        
        if output["step"] == "action":
            function = output["function"]
            fn_input = output["input"]
            print("🔥:" , fn_input)
            if(len(fn_input) == 2):
                fn_output = available_tools[function]["fn"](list(fn_input.values())[0] , list(fn_input.values())[1])
                print("💡 :" , fn_output)
                message.append({"step": "assistant" , "content": json.dumps({"step": "observe", "output": fn_output})})
                continue
            elif(fn_input):
                fn_output = available_tools[function]["fn"](fn_input)
                print("💡 :" , fn_output)
                message.append({"step": "assistant" , "content": json.dumps({"step": "observe", "output": fn_output})})
                continue
            else:
                fn_output = available_tools[function]["fn"]()
                print("💡 :" , fn_output)
                message.append({"step": "assistant" , "content": json.dumps({"step": "observe", "output": fn_output})})
                continue
        
        if output["step"] == "observe":
            print("🧠 :" , output["output"])
            message.append({"step": "assistant" , "content": json.dumps(output)})
            continue
        
        if output["step"] == "output":
            print("🤖:" , output["content"])
            break