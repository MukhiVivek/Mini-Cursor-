A **Mini Command Running Assistant** powered by **Gemini API** that works in **plan → action → observe → output** cycles. You can give it a coding-related command, and it will **plan**, **execute**, and give the result.

## 🚀 How it Works

1. You ask a **coding or system-related query**.
2. The assistant **plans** the required steps to solve it.
3. It **runs system commands** (like creating files, writing code, etc.) on your computer.
4. Shows **output** step-by-step.

Example:
```bash
> make index.js file and write express code in it
```

It will:

-Plan the action

-Run the command to create the file and write code

-Display the result

-Give you confirmation ✅

# 📥 Installation

1️⃣ Clone the repository:

```bash
git clone 
cd
```

2️⃣ Install requirements:

```bash
pip install -r requirements.txt
```

3️⃣ Create .env file with your Gemini API Key:

```bash
Gemini_API=YOUR_API_KEY_HERE
```

4️⃣ Run the project:

```bash
python Cursor.py
```

🎥 Demo Video
📺 [Watch Demo Video](video/demo)

# ⚙️ Features

-Uses Google Gemini API for intelligent planning

-Executes system commands via Python os.system()

-Works in interactive mode

-JSON structured outputs for clear understanding

-Example Use: File Creation, Running Commands, Automation

