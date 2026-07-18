from langchain_core.messages import HumanMessage
from rich.prompt import Prompt
from app.tools.loader import ToolLoader

# ------------------------------------------------------
# Configuration
# ------------------------------------------------------

DEBUG = True

# ------------------------------------------------------
# Load Tools BEFORE Graph
# ------------------------------------------------------

ToolLoader.load_tools()

from app.graph import graph
from app.commands.handler import CommandHandler
from app.llm_manager import llm_manager
from app.configurations.constants import AGENT_NAME
from app.configurations.runtime import runtime_manager
from app.UI import console, show_banner, show_runtime_status, thinking
from app.errors import handle_llm_error


# ------------------------------------------------------
# UI Helpers
# ------------------------------------------------------
from app.UI.renderer import Renderer




def load_models() -> None:
    """
    Load AI models with Rich status indicators.
    """
    with console.status("[info]Loading Planner Model...[/info]") as status:
        llm_manager.get_llm(role="planner")
        status.update("[info]Loading Chat Model...[/info]")
        llm_manager.get_llm(role="chat")
        status.update("[success]✓ Ready[/success]")


def handle_interrupt() -> None:
    """
    Handle user interrupt gracefully.
    """
    console.print()
    console.print("[warning]Session terminated.[/warning]")
    console.print()


# ------------------------------------------------------
# Entry Point
# ------------------------------------------------------


def main() -> None:
    """
    Entry point of the AI Agent.
    """
    
    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------
    
    command_handler = CommandHandler()
    
    # --------------------------------------------------
    # Conversation Memory
    # --------------------------------------------------
    
    conversation = []
    
    # --------------------------------------------------
    # Preload Models
    # --------------------------------------------------
    
    console.print()
    load_models()
    console.print()
    
    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    
    show_banner()
    show_runtime_status()
    
    # --------------------------------------------------
    # Chat Loop
    # --------------------------------------------------
    
    while True:
        try:
            # User prompt
            user_input = Prompt.ask("[user]❯ You[/user]", default="").strip()
            
            # Ignore empty inputs
            if not user_input:
                continue
            
            # ------------------------------------------
            # Exit
            # ------------------------------------------
            
            if user_input.lower() in {"exit", "quit"}:
                console.print()
                console.print("[warning]Goodbye![/warning]")
                console.print()
                break
            
            # ------------------------------------------
            # Framework Commands
            # ------------------------------------------
            
            if command_handler.handle(user_input):
                continue
            
            # ------------------------------------------
            # Conversation
            # ------------------------------------------
            
            conversation.append(HumanMessage(content=user_input))
            state = {"messages": conversation}
            
            # ------------------------------------------
            # Agent
            # ------------------------------------------
            
            try:
                with thinking("Thinking..."):
                    result = graph.invoke(state)
                
                ai_response = result["messages"][-1]
                conversation.append(ai_response)
                
                # Display response
                Renderer.response(ai_response.content)
                
            except Exception as e:
                handle_llm_error(e, debug=DEBUG)
                # Remove the failed message from conversation
                conversation.pop()
        
        except KeyboardInterrupt:
            handle_interrupt()
            break
        
        except EOFError:
            handle_interrupt()
            break
        
        except Exception as e:
            handle_llm_error(e, debug=DEBUG)


if __name__ == "__main__":

    main()