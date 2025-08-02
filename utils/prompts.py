STORY_PROMPT_TEMPLATE = "Write a story about {topic}."

IDEA_GENERATOR_PROMPT_TEMPLATE = """
You are a creative and imaginative story idea generator. Your task is to generate original, compelling, and concise story ideas based on the user's input.

User Input: {user_input}

Please generate 3-5 unique story ideas that are:
1. Original and imaginative - avoid clichés and predictable plots
2. Concise - each idea should be 2-3 sentences maximum
3. Diverse in genre and tone - explore different possibilities
4. Specific enough to inspire a writer but open-ended enough to allow creative development

Format each idea as a numbered list with a brief title and description.
Example:
1. "The Memory Collector" - A woman discovers she can extract and store other people's memories in glass jars. When a mysterious client requests a specific childhood memory, she uncovers a conspiracy.

Be bold, creative, and surprising in your ideas!
"""

print("Prompt templates loaded.")