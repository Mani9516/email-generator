import cohere
import streamlit as st

# Set your Cohere API key
api_key = "1x80ZH7kbo388pl1NneQIAIuIIWhXJb9s4QObRLn"
co = cohere.Client(api_key)

# EmailPrompt class
class EmailPrompt:
    def __init__(self, user_prompt, recipient_name, sender_name, sender_position):
        self.user_prompt = user_prompt
        self.recipient_name = recipient_name
        self.sender_name = sender_name
        self.sender_position = sender_position

    def to_prompt(self):
        return f"""
You are an AI email writer. Write a professional email.

User Prompt: {self.user_prompt}

Recipient:
- Name: {self.recipient_name}

Sender:
- Name: {self.sender_name}
- Position: {self.sender_position}

Write the complete email in a natural, polite tone.
"""
        
# FIXED: Using Chat API instead of Generate API
def generate_email(prompt: EmailPrompt):
    full_prompt = prompt.to_prompt()

    response = co.chat(
        model="command-r",
        message=full_prompt,
        temperature=0.7,
    )

    return response.text.strip()

# Streamlit UI
def main():
    st.title("AI Email Generator (Cohere Chat API)")

    user_prompt = st.text_input("Enter your email prompt:")
    recipient_name = st.text_input("Enter recipient name:")
    sender_name = st.text_input("Enter your name:")
    sender_position = st.text_input("Enter your position:")

    if st.button("Generate Email"):
        if not user_prompt or not recipient_name or not sender_name or not sender_position:
            st.warning("All fields are required!")
        else:
            prompt = EmailPrompt(user_prompt, recipient_name, sender_name, sender_position)
            email_body = generate_email(prompt)
            st.subheader("Generated Email")
            st.text_area("Email Body", value=email_body, height=300)

if __name__ == "__main__":
    main()
