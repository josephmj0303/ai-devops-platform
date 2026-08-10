def build_chat_prompt(prompt: str) -> str:
    return f"""
You are an experienced DevOps Engineer.

Answer the following DevOps question clearly and practically.

Question:

{prompt}
"""
