import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses.tool_choice_options import ToolChoiceOptions
from openai.types.responses.response_text_delta_event import ResponseTextDeltaEvent
from openai.types.responses.response_input_item_param import ResponseInputItemParam


load_dotenv()

# Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "/app/models/Llama/Llama-3.1-8B-Instruct")


client = OpenAI(base_url=OPENAI_API_BASE_URL, api_key=OPENAI_API_KEY)
# models = client.models.list()
# print(f"Available models: {[model.id for model in models]}")


class Chat:
    def __init__(
        self,
        client: OpenAI,
        model: str,
        temperature: float = 0.3,
        tool_choice: ToolChoiceOptions = "none",
        messages: list[ResponseInputItemParam] | None = None,
        stream: bool = True
    ):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.tool_choice : ToolChoiceOptions = tool_choice
        self.messages = messages if messages is not None else []
        self.stream = bool(stream)


    def send(self, message):
        """Sends a message to the chat model and returns the response."""
        
        self.messages.append({"role": "user", "content": message})
        stream = self.client.responses.create(
            model=self.model,
            tool_choice=self.tool_choice,
            input=self.messages,
            temperature=self.temperature,
            stream=self.stream
        )
        assistant_response = ""
        print("Assistant: ", end="", flush=True)
        for event in stream:
                if isinstance(event, ResponseTextDeltaEvent):
                    print(event.delta, end="", flush=True)
                    assistant_response += event.delta
        print("")  # Print a newline after the response is complete
        self.messages.append({"role": "assistant", "content": assistant_response })

        return assistant_response


    def reset(self):
        self.messages = []

def main():
    """Main function to run the chat interface."""
    chatbot = Chat(client=client, model=OPENAI_MODEL)

    while True:
        try:
            user_input = input("You: ").strip()
            cmd = user_input.lower()

            if cmd in ["exit", "quit"]:
                print("\nFin de la conversation.\nMerci d'avoir utilisé le chat !\n")
                break
            if cmd in ["reset", "restart"]:
                chatbot.reset()
                print("Conversation reinitialisee.\n")
                continue
            if not user_input:
                continue

            chatbot.send(user_input)

        except KeyboardInterrupt:
            print("\nArret utilisateur.\n")
            break
        except Exception as e:
            print(f"\nErreur: {e}\n")

if __name__ == "__main__":
    main()