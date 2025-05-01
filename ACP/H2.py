import colorama
from colorama import Fore, Style
from textblob import TextBlob
import time

colorama.init()

def show_processing_animation():
    """Displays a simple loading animation while analyzing sentiment."""
    for _ in range(3):
        print(f"{Fore.CYAN}Analyzing sentiment{'.' * _}{Style.RESET_ALL}", end='\r')
        time.sleep(0.5)

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.25:
        return "Positive", polarity
    elif polarity < -0.25:
        return "Negative", polarity
    else:
        return "Neutral", polarity

def execute_command(command, conversation_history):
    if command.lower() == "summary":
        positive_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Positive")
        negative_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Negative")
        neutral_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Neutral")
        print(f"{Fore.BLUE}📊 Sentiment Analysis Summary:")
        print(f"{Fore.GREEN}Positive: {positive_count}")
        print(f"{Fore.RED}Negative: {negative_count}")
        print(f"{Fore.YELLOW}Neutral: {neutral_count}{Style.RESET_ALL}")
    elif command.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.CYAN}🔄 All conversation history cleared!{Style.RESET_ALL}")
    elif command.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history yet.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}📜 Conversation History:{Style.RESET_ALL}")
            for idx, (text, polarity, sentiment) in enumerate(conversation_history, start=1):
                color = Fore.GREEN if sentiment == "Positive" else Fore.RED if sentiment == "Negative" else Fore.YELLOW
                emoji = "😊" if sentiment == "Positive" else "😢" if sentiment == "Negative" else "😐"
                print(f"{idx}. {color}{emoji} {text}")
                print(f"   (Polarity: {polarity:.2f}, {sentiment}){Style.RESET_ALL}")
    elif command.lower() == "help":
        print(f"{Fore.MAGENTA}Available commands:")
        print(f"  summary - Displays sentiment analysis summary.")
        print(f"  reset - Resets all stored data.")
        print(f"  history - Displays previous messages and their sentiment analyses.")
        print(f"  help - Lists available commands.{Style.RESET_ALL}")

def get_valid_name():
    while True:
        name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}").strip()
        if name.isalpha():
            return name
        else:
            print(f"{Fore.RED}Name must contain only alphabetic characters. Please try again.{Style.RESET_ALL}")

def main():
    print(f"{Fore.CYAN}👋 Welcome to Sentiment Spy! 👋{Style.RESET_ALL}")
    user_name = get_valid_name()
    print(f"{Fore.CYAN}Hello, Agent {user_name}!{Style.RESET_ALL}")
    print(f"Type any sentence and I'll analyze its sentiment. 😊")
    print(f"Type {Fore.YELLOW}summary{Fore.CYAN}, {Fore.YELLOW}reset{Fore.CYAN}, {Fore.YELLOW}history{Fore.CYAN}, {Fore.YELLOW}help{Fore.CYAN}, or {Fore.YELLOW}exit{Fore.CYAN} to quit.{Style.RESET_ALL}")

    conversation_history = []

    while True:
        user_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()

        if not user_input:
            print(f"{Fore.RED}Please enter some text or a valid command.{Style.RESET_ALL}")
            continue

        if user_input.lower() == "exit":
            print(f"\n{Fore.BLUE}👋 Exiting Sentiment Spy. Farewell, Agent {user_name}! 👋{Style.RESET_ALL}")
            positive_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Positive")
            negative_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Negative")
            neutral_count = sum(1 for _, _, sentiment in conversation_history if sentiment == "Neutral")
            with open(f"{user_name}_sentiment_analysis.txt", "w") as file:
                file.write(f"Sentiment Analysis Summary for {user_name}\n")
                file.write(f"Positive: {positive_count}\n")
                file.write(f"Negative: {negative_count}\n")
                file.write(f"Neutral: {neutral_count}\n")
            print(f"{Fore.CYAN}📄 Summary saved to {user_name}_sentiment_analysis.txt{Style.RESET_ALL}\n")
            break

        if user_input.lower() in {"summary", "reset", "history", "help"}:
            execute_command(user_input, conversation_history)
            continue

        show_processing_animation()
        sentiment, polarity = analyze_sentiment(user_input)
        color = Fore.GREEN if sentiment == "Positive" else Fore.RED if sentiment == "Negative" else Fore.YELLOW
        emoji = "😊" if sentiment == "Positive" else "😢" if sentiment == "Negative" else "😐"
        conversation_history.append((user_input, polarity, sentiment))
        print(f"{color}{emoji} {sentiment} sentiment detected!")
        print(f"(Polarity: {polarity:.2f}){Style.RESET_ALL}")

if __name__ == "__main__":
    main()
