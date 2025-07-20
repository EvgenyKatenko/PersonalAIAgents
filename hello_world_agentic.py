from agents import Agent, Runner
from dotenv import load_dotenv


def main():
    agent = Agent(name="Assistant", instructions="You are funny commedian")
    result = Runner.run_sync(agent, "Say hello world in a funny way")
    print(result.final_output)

if __name__ == "__main__":
    load_dotenv(override=True)
    main()
