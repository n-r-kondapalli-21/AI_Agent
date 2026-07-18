# AI Agent - Complete Project Documentation

---

## 1. Project Overview

### What Problem This Project Solves

This project solves the problem of building an AI agent that can decide when to use external tools (like web search) versus answering from its own knowledge. Many AI systems either always use tools or never use them. This project creates a smart decision-making system that analyzes each user question and determines whether external information is needed.

### Why This Architecture Was Chosen

The architecture uses **LangGraph**, which is a framework for building stateful, multi-actor applications with LLMs. LangGraph was chosen because:

- It provides a clean way to define workflows as graphs with nodes and edges
- It manages state automatically between different steps
- It supports conditional routing (deciding which path to take based on the current state)
- It makes the agent's decision process visible and debuggable

### Main Design Philosophy

The project follows these core principles:

1. **Separation of Concerns**: Each component has one clear job
   - Planner decides whether to use a tool
   - Tools execute specific actions
   - Chat generates the final response
   - Router directs traffic between components

2. **Plugin Architecture**: Tools are designed as plugins that can be added without modifying core code

3. **State Management**: All components share a common state object, making data flow transparent

4. **Type Safety**: Pydantic models ensure data consistency throughout the system

### High-Level Workflow

```
User Input
    |
    v
Conversation Manager
    |
    v
LangGraph Workflow
    |
    v
Planner Node (Should we use a tool?)
    |
    +-------------------+
    |                   |
    v                   v
Yes (Use Tool)     No (Answer directly)
    |                   |
    v                   |
Search Node          |
    |                   |
    v                   |
Tool Manager         |
    |                   |
    v                   |
Tool Registry         |
    |                   |
    v                   |
Search Tool           |
    |                   |
    +-------------------+
    |
    v
Prompt Builder
    |
    v
Chat Node
    |
    v
LLM (OpenRouter)
    |
    v
Final Response to User
```

---

## 2. Project Folder Structure

```
d:\My_Ai_Agent/
│
├── main.py                 # Entry point - starts the agent
├── requirements.txt        # Python dependencies
├── README.md              # Project description
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
│
├── app/                   # Main application package
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── llm.py             # LLM initialization
│   ├── state.py           # Shared state definition
│   ├── schema.py          # Data models (Pydantic)
│   ├── enums.py           # Enumerations
│   ├── conversation.py    # Conversation history manager
│   ├── router.py          # Routing logic
│   ├── tool_manager.py    # Central tool execution manager
│   ├── graph.py           # LangGraph workflow definition
│   ├── utils.py           # Utility functions
│   ├── exceptions.py      # Custom exceptions
│   │
│   ├── nodes/             # Graph nodes (workflow steps)
│   │   ├── __init__.py
│   │   ├── planner.py     # Decision-making node
│   │   ├── chat.py        # Response generation node
│   │   └── search.py      # Tool execution node
│   │
│   ├── chains/            # LangChain chains
│   │   ├── planner.py     # Planner LLM chain
│   │   └── chat.py        # Chat LLM chain
│   │
│   ├── prompts/           # Prompt templates
│   │   ├── __init__.py
│   │   ├── planner.py     # Planner system prompt
│   │   └── chat.py        # Chat system prompt
│   │
│   ├── builders/          # Data builders
│   │   ├── __init__.py
│   │   └── prompt_builder.py  # Builds prompt data
│   │
│   └── tools/             # Tool plugin system
│       ├── __init__.py
│       ├── base.py        # Abstract base class for tools
│       ├── registry.py    # Tool registration system
│       ├── loader.py      # Tool loader
│       └── search_tool.py # DuckDuckGo search implementation
│
├── tests/                 # Test files
│
├── test_planner.py        # Planner tests
├── test_search_node.py    # Search node tests
│
└── venv/                  # Virtual environment
```

### Folder Explanations

#### `app/` - Main Application Package

**Purpose**: Contains all the core application code.

**Responsibilities**:
- Defines the agent's architecture
- Implements the workflow graph
- Manages tools and their execution
- Handles LLM integration
- Maintains conversation state

**Why it exists**: Organizes all application code in a single package for clean imports and modularity.

**Which files depend on it**: `main.py` imports from `app/`. Everything inside `app/` depends on other modules within `app/`.

#### `app/nodes/` - Graph Nodes

**Purpose**: Contains the individual steps (nodes) in the LangGraph workflow.

**Responsibilities**:
- `planner.py`: Decides whether to use a tool
- `chat.py`: Generates the final AI response
- `search.py`: Executes the selected tool

**Why it exists**: Separates each workflow step into its own file, making the code easier to understand and test.

**Which files depend on it**: `app/graph.py` imports and registers these nodes.

#### `app/chains/` - LangChain Chains

**Purpose**: Contains LangChain chains that combine prompts with LLMs.

**Responsibilities**:
- `planner.py`: Creates the chain that makes planning decisions
- `chat.py`: Creates the chain that generates responses

**Why it exists**: Encapsulates the prompt + LLM combination pattern used by LangChain.

**Which files depend on it**: `app/nodes/planner.py` and `app/nodes/chat.py` use these chains.

#### `app/prompts/` - Prompt Templates

**Purpose**: Stores the system prompts that define AI behavior.

**Responsibilities**:
- `planner.py`: Defines how the planner should think
- `chat.py`: Defines how the chat assistant should respond

**Why it exists**: Separates prompt text from code logic, making it easy to tweak AI behavior without changing code.

**Which files depend on it**: `app/chains/` imports these prompts.

#### `app/builders/` - Data Builders

**Purpose**: Constructs complex data objects needed by other components.

**Responsibilities**:
- `prompt_builder.py`: Builds the prompt data dictionary for the chat chain

**Why it exists**: Centralizes data construction logic, keeping nodes clean and focused.

**Which files depend on it**: `app/nodes/chat.py` uses the PromptBuilder.

#### `app/tools/` - Tool Plugin System

**Purpose**: Implements a plugin architecture for adding new capabilities.

**Responsibilities**:
- `base.py`: Defines the interface all tools must implement
- `registry.py`: Manages tool registration and retrieval
- `loader.py`: Loads and registers all available tools
- `search_tool.py`: Implements web search using DuckDuckGo

**Why it exists**: Allows new tools to be added without modifying core agent code.

**Which files depend on it**: `app/tool_manager.py` and `app/nodes/search.py` use the tool system.

---

## 3. Folder-by-Folder Explanation

### `main.py` → `app/`

```
main.py
    |
    v
app/graph.py
    |
    v
app/nodes/
    |
    v
app/chains/
    |
    v
app/prompts/
    |
    v
app/llm.py
```

**Purpose**: Entry point that initializes the system and runs the main loop.

**Responsibilities**:
- Load tools
- Start the conversation loop
- Invoke the graph
- Display results

**Files inside**: Only `main.py` itself

**How it communicates**: Imports `graph` from `app/graph.py` and `ToolLoader` from `app/tools/loader.py`.

### `app/graph.py` → `app/nodes/`

```
app/graph.py
    |
    v
app/nodes/planner.py
    |
    v
app/nodes/search.py
    |
    v
app/nodes/chat.py
```

**Purpose**: Defines the workflow structure using LangGraph.

**Responsibilities**:
- Create the StateGraph
- Register all nodes
- Connect nodes with edges
- Add conditional routing
- Compile the final graph

**Files inside**: Only `graph.py` itself

**How it communicates**: Imports node functions from `app/nodes/` and the router from `app/router.py`.

### `app/nodes/` → `app/chains/` and `app/builders/`

```
app/nodes/planner.py
    |
    v
app/chains/planner.py
    |
    v
app/prompts/planner.py
    |
    v
app/llm.py

app/nodes/chat.py
    |
    v
app/builders/prompt_builder.py
    |
    v
app/chains/chat.py
    |
    v
app/prompts/chat.py
    |
    v
app/llm.py

app/nodes/search.py
    |
    v
app/tool_manager.py
    |
    v
app/tools/
```

**Purpose**: Each node implements one step in the workflow.

**Responsibilities**:
- Receive state as input
- Perform their specific task
- Return updated state

**Files inside**: `planner.py`, `chat.py`, `search.py`

**How it communicates**:
- Planner node uses planner chain
- Chat node uses PromptBuilder and chat chain
- Search node uses ToolManager

### `app/chains/` → `app/prompts/` and `app/llm.py`

```
app/chains/planner.py
    |
    v
app/prompts/planner.py
    |
    v
app/llm.py

app/chains/chat.py
    |
    v
app/prompts/chat.py
    |
    v
app/llm.py
```

**Purpose**: Combines prompts with LLMs to create executable chains.

**Responsibilities**:
- Import the appropriate prompt
- Initialize the LLM
- Create the chain using the pipe operator (|)

**Files inside**: `planner.py`, `chat.py`

**How it communicates**: Imports prompts from `app/prompts/` and LLM from `app/llm.py`.

### `app/prompts/` → No dependencies

```
app/prompts/planner.py (standalone)
app/prompts/chat.py (standalone)
```

**Purpose**: Define the system prompts that guide AI behavior.

**Responsibilities**:
- Define the system message
- Define available tools
- Set behavior guidelines

**Files inside**: `planner.py`, `chat.py`

**How it communicates**: No dependencies. These are pure data definitions.

### `app/builders/` → `app/tool_manager.py`

```
app/builders/prompt_builder.py
    |
    v
app/tool_manager.py
    |
    v
app/tools/registry.py
```

**Purpose**: Constructs complex data objects.

**Responsibilities**:
- Build prompt data dictionary
- Format tool results for prompts

**Files inside**: `prompt_builder.py`

**How it communicates**: Uses ToolManager to format tool results.

### `app/tools/` → Self-contained system

```
app/tools/base.py (interface)
    |
    v
app/tools/search_tool.py (implementation)
    |
    v
app/tools/registry.py (storage)
    |
    v
app/tools/loader.py (initialization)
```

**Purpose**: Plugin architecture for adding new capabilities.

**Responsibilities**:
- Define tool interface
- Implement specific tools
- Register and manage tools
- Load tools at startup

**Files inside**: `base.py`, `registry.py`, `loader.py`, `search_tool.py`

**How it communicates**: The tool system is mostly self-contained. Other parts of the app interact through ToolManager.

---

## 4. File-by-File Documentation

### `main.py`

**Purpose**: Entry point of the application. Starts the agent and runs the conversation loop.

**Responsibilities**:
- Load and register all tools
- Display welcome message
- Run conversation loop
- Get user input
- Invoke the graph
- Display AI responses
- Handle errors

**Classes**: None

**Functions**:
- `main()`: Main function that runs the application

**Inputs**: User input from console

**Outputs**: AI responses to console

**Dependencies**:
- `langchain_core.messages.HumanMessage`
- `app.graph.graph`
- `app.tools.loader.ToolLoader`

**Produces**: Interactive conversation with the user

---

### `app/graph.py`

**Purpose**: Defines the LangGraph workflow structure.

**Responsibilities**:
- Create a StateGraph with AgentState
- Register three nodes: planner, search, chat
- Connect START to planner
- Add conditional edges from planner
- Connect search to chat
- Connect chat to END
- Compile the graph

**Classes**: None

**Functions**: None (module-level code)

**Inputs**: None (defines graph structure)

**Outputs**: Compiled `graph` object

**Dependencies**:
- `langgraph.graph.StateGraph, START, END`
- `app.state.AgentState`
- `app.nodes.planner.planner_node`
- `app.nodes.chat.chat_node`
- `app.nodes.search.search_node`
- `app.router.planner_router`

**Produces**: A compiled LangGraph that can be invoked with state

---

### `app/state.py`

**Purpose**: Defines the shared state object that passes between graph nodes.

**Responsibilities**:
- Define the structure of AgentState
- Specify which fields are required vs optional

**Classes**:
- `AgentState`: TypedDict containing:
  - `messages`: List of conversation messages (required)
  - `planner_decision`: Decision from planner (optional)
  - `tool_result`: Result from tool execution (optional)

**Functions**: None

**Inputs**: None (type definition only)

**Outputs**: Type definition

**Dependencies**:
- `typing_extensions.TypedDict, NotRequired`
- `langchain_core.messages.BaseMessage`
- `app.schema.PlannerDecision, ToolResult`

**Produces**: Type definition used by all nodes

---

### `app/schema.py`

**Purpose**: Defines all data models using Pydantic for type safety and validation.

**Responsibilities**:
- Define structured data models
- Ensure data consistency
- Provide clear data contracts

**Classes**:
- `ToolRequest`: Request sent to execute a tool
  - `tool_name`: Which tool to use
  - `parameters`: Tool-specific parameters

- `ToolResult`: Standard response from any tool
  - `success`: Whether execution succeeded
  - `tool_name`: Which tool produced this
  - `content`: The actual result data
  - `error`: Error message if failed

- `SearchItem`: Single search result
  - `title`: Result title
  - `url`: Result URL
  - `snippet`: Result snippet

- `SearchResult`: Complete search response
  - `query`: Original search query
  - `results`: List of SearchItem objects

- `PlannerDecision`: Decision from the planner
  - `use_tool`: Whether to use a tool
  - `tool_request`: Which tool to use (if any)
  - `reasoning`: Why this decision was made
  - `final_answer`: Direct answer if no tool needed

**Functions**: None

**Inputs**: None (model definitions)

**Outputs**: Pydantic model classes

**Dependencies**:
- `typing.Any`
- `pydantic.BaseModel, Field`
- `app.enums.ToolName`

**Produces**: Data models used throughout the application

---

### `app/conversation.py`

**Purpose**: Manages conversation history (currently not used in main.py but available).

**Responsibilities**:
- Store conversation messages
- Add user messages
- Add AI messages
- Retrieve message history
- Clear conversation
- Count messages

**Classes**:
- `ConversationManager`: Manages the message list
  - `_messages`: Internal list of messages

**Functions**:
- `add_user_message(content)`: Add a user message
- `add_ai_message(message)`: Add an AI message
- `get_messages()`: Get all messages
- `clear()`: Clear all messages
- `message_count()`: Get message count

**Inputs**: Message content or AIMessage objects

**Outputs**: Message lists or counts

**Dependencies**:
- `langchain_core.messages.HumanMessage, AIMessage, BaseMessage`

**Produces**: Managed conversation history

---

### `app/config.py`

**Purpose**: Centralizes configuration settings from environment variables.

**Responsibilities**:
- Load environment variables from .env file
- Provide default values
- Expose settings as a class

**Classes**:
- `Settings`: Configuration class
  - `BASE_URL`: LLM API base URL
  - `PROVIDER`: LLM provider name
  - `MODEL_NAME`: Model to use
  - `OPENROUTER_API_KEY`: API key
  - `TEMPERATURE`: LLM temperature
  - `MAX_TOKENS`: Maximum tokens

**Functions**: None

**Inputs**: Environment variables

**Outputs**: Settings instance

**Dependencies**:
- `dotenv.load_dotenv`
- `os`

**Produces**: Configuration settings used by `app/llm.py`

---

### `app/enums.py`

**Purpose**: Defines enumerations for type-safe constants.

**Responsibilities**:
- Define tool names as enum
- Define node names as enum
- Prevent string typos

**Classes**:
- `ToolName`: Available tools
  - SEARCH
  - CALCULATOR
  - PYTHON
  - FILESYSTEM
  - BROWSER
  - SQL
  - WIKIPEDIA

- `NodeName`: Graph node names
  - PLANNER
  - CHAT
  - SEARCH

**Functions**: None

**Inputs**: None

**Outputs**: Enum definitions

**Dependencies**:
- `enum.Enum`

**Produces**: Type-safe constants used throughout the app

---

### `app/router.py`

**Purpose**: Determines which node to execute next based on planner decision.

**Responsibilities**:
- Read the planner decision from state
- Return the next node name
- Route to tool node if tool is needed
- Route to chat node if no tool needed

**Classes**: None

**Functions**:
- `planner_router(state)`: Route based on decision

**Inputs**: AgentState containing planner_decision

**Outputs**: String name of next node

**Dependencies**:
- `app.state.AgentState`
- `app.enums.NodeName`

**Produces**: Routing decision for LangGraph

---

### `app/llm.py`

**Purpose**: Initializes and configures the LLM client.

**Responsibilities**:
- Create LLM instance based on provider
- Configure model parameters
- Handle different providers

**Classes**: None

**Functions**:
- `get_llm()`: Return configured LLM instance

**Inputs**: None (reads from config)

**Outputs`: ChatOpenAI instance

**Dependencies**:
- `langchain_openai.ChatOpenAI`
- `app.config.settings`

**Produces**: LLM instance used by chains

---

### `app/tool_manager.py`

**Purpose**: Central manager for executing tools and formatting their results.

**Responsibilities**:
- Execute tool requests
- Format tool results for prompts
- Act as interface to tool registry

**Classes**:
- `ToolManager`: Tool execution manager

**Functions**:
- `execute(request)`: Execute a tool request
- `format(tool_result)`: Format tool result for prompt

**Inputs**: ToolRequest or ToolResult

**Outputs**: ToolResult or formatted string

**Dependencies**:
- `app.schema.ToolRequest, ToolResult`
- `app.tools.registry.tool_registry`

**Produces**: Tool execution and formatting services

---

### `app/nodes/planner.py`

**Purpose**: Graph node that decides whether to use a tool.

**Responsibilities**:
- Invoke the planner chain
- Get decision from LLM
- Add decision to state

**Classes**: None

**Functions**:
- `planner_node(state)`: Make planning decision

**Inputs**: AgentState with messages

**Outputs**: Updated AgentState with planner_decision

**Dependencies**:
- `app.chains.planner.planner_chain`
- `app.state.AgentState`

**Produces**: Planning decision added to state

---

### `app/nodes/chat.py`

**Purpose**: Graph node that generates the final AI response.

**Responsibilities**:
- Build prompt data
- Invoke chat chain
- Add response to messages

**Classes**: None

**Functions**:
- `chat_node(state)`: Generate response

**Inputs**: AgentState with messages and optional tool_result

**Outputs**: Updated AgentState with new message

**Dependencies**:
- `app.builders.prompt_builder.PromptBuilder`
- `app.chains.chat.chat_chain`
- `app.state.AgentState`

**Produces**: AI response message

---

### `app/nodes/search.py`

**Purpose**: Graph node that executes the selected tool.

**Responsibilities**:
- Extract tool request from state
- Execute tool via ToolManager
- Store result in state

**Classes**: None

**Functions**:
- `search_node(state)`: Execute tool

**Inputs**: AgentState with planner_decision

**Outputs**: Updated AgentState with tool_result

**Dependencies**:
- `app.state.AgentState`
- `app.tool_manager.ToolManager`

**Produces**: Tool execution result

---

### `app/chains/planner.py`

**Purpose**: Creates the LangChain chain for planning decisions.

**Responsibilities**:
- Initialize LLM
- Combine prompt with LLM
- Configure structured output

**Classes**: None

**Functions**: None (module-level chain creation)

**Inputs**: Messages dictionary

**Outputs**: PlannerDecision object

**Dependencies**:
- `app.llm.get_llm`
- `app.prompts.planner.planner_prompt`
- `app.schema.PlannerDecision`

**Produces**: planner_chain used by planner node

**Note**: Uses `with_structured_output()` to force LLM to return valid PlannerDecision

---

### `app/chains/chat.py`

**Purpose**: Creates the LangChain chain for generating responses.

**Responsibilities**:
- Initialize LLM
- Combine prompt with LLM

**Classes**: None

**Functions**: None (module-level chain creation)

**Inputs**: Prompt data dictionary

**Outputs`: AIMessage object

**Dependencies**:
- `app.llm.get_llm`
- `app.prompts.chat.chat_prompt`

**Produces**: chat_chain used by chat node

---

### `app/prompts/planner.py`

**Purpose**: Defines the system prompt for the planner.

**Responsibilities**:
- Define planner's role
- List available tools
- Explain when to use tools
- Instruct on output format

**Classes**: None

**Functions**: None (module-level prompt definition)

**Inputs**: None

**Outputs**: ChatPromptTemplate object

**Dependencies**:
- `langchain_core.prompts.ChatPromptTemplate`

**Produces**: planner_prompt used by planner chain

---

### `app/prompts/chat.py`

**Purpose**: Defines the system prompt for the chat assistant.

**Responsibilities**:
- Define assistant's role
- Explain how to use tool context
- Set behavior guidelines

**Classes**: None

**Functions**: None (module-level prompt definition)

**Inputs**: None

**Outputs**: ChatPromptTemplate object

**Dependencies**:
- `langchain_core.prompts.ChatPromptTemplate`

**Produces**: chat_prompt used by chat chain

---

### `app/builders/prompt_builder.py`

**Purpose**: Builds the prompt data dictionary for the chat chain.

**Responsibilities**:
- Extract messages from state
- Check for tool result
- Format tool result if present
- Build complete prompt data

**Classes**:
- `PromptBuilder`: Prompt data builder

**Functions**:
- `build(state)`: Build prompt data dictionary

**Inputs**: AgentState

**Outputs**: Dictionary with messages and tool_context

**Dependencies**:
- `app.state.AgentState`
- `app.tool_manager.ToolManager`

**Produces**: Prompt data for chat chain

---

### `app/tools/base.py`

**Purpose**: Defines the abstract interface that all tools must implement.

**Responsibilities**:
- Define tool interface
- Enforce implementation of required methods
- Provide common tool attributes

**Classes**:
- `BaseTool`: Abstract base class
  - `name`: Tool name
  - `description`: Tool description
  - `run(**kwargs)`: Execute the tool (abstract)
  - `format_for_prompt(result)`: Format result for prompt (abstract)

**Functions**: None

**Inputs**: Tool name and description in constructor

**Outputs**: ToolResult from run(), string from format_for_prompt()

**Dependencies**:
- `abc.ABC, abstractmethod`
- `app.enums.ToolName`
- `app.schema.ToolResult`

**Produces**: Interface that all tools must implement

---

### `app/tools/registry.py`

**Purpose**: Stores and manages all registered tools.

**Responsibilities**:
- Store tools in a dictionary
- Register new tools
- Retrieve tools by name
- Check if tool exists
- List all tools

**Classes**:
- `ToolRegistry`: Tool storage and management
  - `_tools`: Internal dictionary of tools

**Functions**:
- `register(tool)`: Register a tool
- `get(tool_name)`: Retrieve a tool
- `exists(tool_name)`: Check if tool exists
- `list_tools()`: Get all tools
- `list_tool_names()`: Get all tool names

**Inputs**: BaseTool objects or ToolName enums

**Outputs**: BaseTool objects, booleans, or lists

**Dependencies**:
- `app.enums.ToolName`
- `app.tools.base.BaseTool`

**Produces**: Global `tool_registry` instance

---

### `app/tools/loader.py`

**Purpose**: Loads and registers all available tools at startup.

**Responsibilities**:
- Import all tool classes
- Instantiate tools
- Register tools in registry

**Classes**:
- `ToolLoader`: Tool loading coordinator

**Functions**:
- `load_tools()`: Load and register all tools

**Inputs**: None

**Outputs**: None (side effect: registers tools)

**Dependencies**:
- `app.tools.registry.tool_registry`
- `app.tools.search_tool.DuckDuckGoSearchTool`

**Produces**: Registered tools in the global registry

---

### `app/tools/search_tool.py`

**Purpose**: Implements web search using DuckDuckGo.

**Responsibilities**:
- Search the web using DuckDuckGo API
- Parse search results
- Convert to structured format
- Format results for prompts

**Classes**:
- `DuckDuckGoSearchTool`: Web search implementation

**Functions**:
- `run(query, max_results)`: Execute search
- `format_for_prompt(result)`: Format search results

**Inputs**: Search query and max results

**Outputs**: ToolResult with SearchResult content

**Dependencies**:
- `ddgs.DDGS`
- `app.enums.ToolName`
- `app.schema.ToolResult, SearchItem, SearchResult`
- `app.tools.base.BaseTool`

**Produces**: Web search capability

---

## 5. Execution Flow

### What Happens When User Types "Latest AI news"

```
User types: "Latest AI news"
    |
    v
Step 1: main.py reads input
    |
    v
Step 2: main.py creates HumanMessage
    |
    v
Step 3: main.py creates state with messages
    |
    v
Step 4: main.py invokes graph with state
    |
    v
Step 5: LangGraph executes planner_node
    |
    v
Step 6: planner_node calls planner_chain
    |
    v
Step 7: planner_chain combines prompt + LLM
    |
    v
Step 8: LLM analyzes the question
    |
    v
Step 9: LLM returns PlannerDecision
    {
        "use_tool": true,
        "tool_request": {
            "tool_name": "search",
            "parameters": {"query": "Latest AI news"}
        },
        "reasoning": "This requires current information"
    }
    |
    v
Step 10: planner_node adds decision to state
    |
    v
Step 11: LangGraph calls planner_router
    |
    v
Step 12: planner_router sees use_tool=true
    |
    v
Step 13: planner_router returns "search"
    |
    v
Step 14: LangGraph executes search_node
    |
    v
Step 15: search_node calls ToolManager.execute()
    |
    v
Step 16: ToolManager gets tool from registry
    |
    v
Step 17: ToolManager calls DuckDuckGoSearchTool.run()
    |
    v
Step 18: DuckDuckGoSearchTool searches web
    |
    v
Step 19: DuckDuckGoSearchTool returns ToolResult
    {
        "success": true,
        "tool_name": "search",
        "content": SearchResult with news items
    }
    |
    v
Step 20: search_node adds tool_result to state
    |
    v
Step 21: LangGraph routes to chat_node
    |
    v
Step 22: chat_node calls PromptBuilder.build()
    |
    v
Step 23: PromptBuilder extracts tool_result
    |
    v
Step 24: PromptBuilder calls ToolManager.format()
    |
    v
Step 25: ToolManager calls DuckDuckGoSearchTool.format_for_prompt()
    |
    v
Step 26: Formatted search results added to prompt
    |
    v
Step 27: chat_node calls chat_chain
    |
    v
Step 28: chat_chain combines prompt + LLM
    |
    v
Step 29: LLM reads search results
    |
    v
Step 30: LLM generates response based on search results
    |
    v
Step 31: LLM returns AIMessage
    |
    v
Step 32: chat_node adds AIMessage to state
    |
    v
Step 33: LangGraph reaches END
    |
    v
Step 34: graph returns final state to main.py
    |
    v
Step 35: main.py extracts last message
    |
    v
Step 36: main.py displays response to user
    |
    v
User sees: "Here are the latest AI news stories..."
```

### Plain English Explanation

1. **User Input**: You type "Latest AI news" and press enter.

2. **Message Creation**: The system wraps your text in a HumanMessage object. This is a standard format that LangChain uses to represent messages from humans.

3. **State Preparation**: The system creates a state dictionary containing your message. This state is like a suitcase that will travel through the entire workflow, collecting information along the way.

4. **Graph Invocation**: The system hands the state to the LangGraph. Think of the graph as a factory assembly line where each station (node) does a specific job.

5. **Planner Execution**: The first station is the Planner. Its job is to decide: "Do we need to use a tool for this question?"

6. **Planner Chain**: The Planner uses a chain that combines a system prompt with the LLM. The system prompt tells the LLM: "You are a planner. Decide if we need to search the web."

7. **LLM Analysis**: The LLM reads your question and thinks: "This asks for latest news. News changes constantly. I don't have current information in my training. I should search."

8. **Structured Decision**: The LLM returns a structured decision object (not just text). This object says: "Yes, use the search tool with query 'Latest AI news'."

9. **Router Decision**: The router looks at this decision and sees that a tool is needed. It directs the workflow to the search node.

10. **Tool Execution**: The search node receives the decision and asks the ToolManager to execute the search.

11. **Tool Lookup**: The ToolManager checks the registry and finds the DuckDuckGoSearchTool.

12. **Web Search**: The search tool connects to DuckDuckGo and searches for "Latest AI news".

13. **Result Processing**: The search tool receives raw results from DuckDuckGo and converts them into a structured SearchResult object with titles, URLs, and snippets.

14. **Result Storage**: The search result is added to the state. Now the state contains: your original message, the planner's decision, and the search results.

15. **Prompt Building**: The workflow moves to the chat node. The PromptBuilder looks at the state and sees there are search results. It formats these results into readable text.

16. **Response Generation**: The chat chain combines the formatted search results with the chat system prompt. The system prompt tells the LLM: "You are a helpful assistant. Use the search results as your source of truth."

17. **Final Response**: The LLM reads the search results and generates a summary: "Here are the latest AI news stories: [summarizes the search results]."

18. **Message Addition**: This response is added to the state as an AIMessage.

19. **Completion**: The workflow reaches the END node and returns the final state to main.py.

20. **Display**: main.py extracts the last message (the AI's response) and displays it to you.

---

## 6. Data Flow

### How Data Moves Through the System

```
User Input (String)
    |
    v
HumanMessage (LangChain object)
    |
    v
AgentState (Dictionary)
    {
        "messages": [HumanMessage]
    }
    |
    v
Planner Chain Input
    {
        "messages": [HumanMessage]
    }
    |
    v
PlannerDecision (Pydantic model)
    {
        "use_tool": true,
        "tool_request": ToolRequest {...},
        "reasoning": "..."
    }
    |
    v
AgentState (Updated)
    {
        "messages": [HumanMessage],
        "planner_decision": PlannerDecision {...}
    }
    |
    v
ToolRequest (Pydantic model)
    {
        "tool_name": ToolName.SEARCH,
        "parameters": {"query": "..."}
    }
    |
    v
ToolManager.execute()
    |
    v
DuckDuckGoSearchTool.run()
    |
    v
ToolResult (Pydantic model)
    {
        "success": true,
        "tool_name": ToolName.SEARCH,
        "content": SearchResult {...}
    }
    |
    v
AgentState (Updated)
    {
        "messages": [HumanMessage],
        "planner_decision": PlannerDecision {...},
        "tool_result": ToolResult {...}
    }
    |
    v
PromptBuilder.build()
    |
    v
Prompt Data (Dictionary)
    {
        "messages": [HumanMessage],
        "tool_context": "Search Query: ...\nSearch Results:\n..."
    }
    |
    v
Chat Chain Input
    {
        "messages": [HumanMessage],
        "tool_context": "..."
    }
    |
    v
AIMessage (LangChain object)
    {
        "content": "Here are the latest AI news..."
    }
    |
    v
AgentState (Final)
    {
        "messages": [HumanMessage, AIMessage],
        "planner_decision": PlannerDecision {...},
        "tool_result": ToolResult {...}
    }
    |
    v
main.py extracts AIMessage
    |
    v
User sees response text
```

### Data Transformation Summary

1. **String → HumanMessage**: User input is wrapped in a LangChain message object
2. **HumanMessage → AgentState**: Message is placed in state dictionary
3. **AgentState → PlannerDecision**: LLM analyzes and makes decision
4. **PlannerDecision → ToolRequest**: Decision is converted to tool request
5. **ToolRequest → ToolResult**: Tool executes and returns result
6. **ToolResult → String**: Result is formatted for prompt
7. **String → AIMessage**: LLM generates response message
8. **AIMessage → String**: Response is displayed to user

---

## 7. Folder Interaction Diagram

```
main.py
    |
    v
app/graph.py
    |
    v
app/nodes/
    |
    +-----------------------+
    |                       |
    v                       v
app/chains/          app/tool_manager.py
    |                       |
    v                       v
app/prompts/         app/tools/
    |                       |
    v                       |
app/llm.py             app/tools/registry.py
    |                       |
    v                       |
app/config.py         app/tools/base.py
```

### Interaction Flow

1. **main.py** starts everything
2. **app/graph.py** defines the workflow
3. **app/nodes/** implement workflow steps
4. **app/chains/** connect prompts to LLMs
5. **app/prompts/** define AI behavior
6. **app/llm.py** provides LLM instances
7. **app/config.py** provides configuration
8. **app/tool_manager.py** executes tools
9. **app/tools/** implement tool plugins
10. **app/tools/registry.py** manages tools
11. **app/tools/base.py** defines tool interface

---

## 8. Class Diagram

### ToolManager

**Purpose**: Central coordinator for tool execution.

**Used by**:
- `app/nodes/search.py` (to execute tools)
- `app/builders/prompt_builder.py` (to format results)

**Uses**:
- `app/tools.registry.tool_registry` (to get tools)
- `app.schema.ToolRequest` (input format)
- `app.schema.ToolResult` (output format)

**Returns**:
- `ToolResult` from `execute()`
- Formatted string from `format()`

---

### ToolRegistry

**Purpose**: Stores and provides access to registered tools.

**Used by**:
- `app/tool_manager.py` (to get tools)
- `app/tools/loader.py` (to register tools)

**Uses**:
- `app.tools.base.BaseTool` (stores instances)
- `app.enums.ToolName` (dictionary keys)

**Returns**:
- `BaseTool` instances from `get()`
- Lists of tools from `list_tools()`

---

### BaseTool

**Purpose**: Abstract interface that all tools must implement.

**Used by**:
- `app/tools/search_tool.py` (inherits from it)
- `app/tools.registry.ToolRegistry` (stores instances)

**Uses**:
- `app.enums.ToolName` (tool name)
- `app.schema.ToolResult` (return type)

**Returns**:
- `ToolResult` from `run()`
- String from `format_for_prompt()`

---

### DuckDuckGoSearchTool

**Purpose**: Concrete implementation of web search.

**Used by**:
- `app/tools/loader.py` (instantiated and registered)

**Uses**:
- `app.tools.base.BaseTool` (inherits)
- `app.enums.ToolName` (tool name)
- `app.schema.ToolResult, SearchItem, SearchResult` (data models)
- `ddgs.DDGS` (search API)

**Returns**:
- `ToolResult` with `SearchResult` content

---

### PromptBuilder

**Purpose**: Constructs prompt data for the chat chain.

**Used by**:
- `app/nodes/chat.py` (builds prompt data)

**Uses**:
- `app.state.AgentState` (input)
- `app.tool_manager.ToolManager` (format results)

**Returns**:
- Dictionary with `messages` and `tool_context`

---

### ConversationManager

**Purpose**: Manages conversation history (available but not currently used).

**Used by**:
- Could be used by `main.py` in future

**Uses**:
- `langchain_core.messages` (message types)

**Returns**:
- Message lists from `get_messages()`
- Counts from `message_count()`

---

### Settings

**Purpose**: Configuration container.

**Used by**:
- `app/llm.py` (reads configuration)

**Uses**:
- `os` (environment variables)
- `dotenv` (load .env file)

**Returns**:
- Configuration values as class attributes

---

## 9. Object Lifecycle

### PlannerDecision Lifecycle

```
Creation
    |
    v
planner_chain.invoke() returns PlannerDecision
    |
    v
planner_node adds to state
    |
    v
planner_router reads from state
    |
    v
search_node reads tool_request from decision
    |
    v
Decision no longer needed after tool execution
    |
    v
Garbage collected when state is replaced
```

**Purpose**: Represents the planner's decision about whether to use a tool.

**Created by**: `app/chains/planner.py` (LLM with structured output)

**Used by**: 
- `app/router.py` (to determine next node)
- `app/nodes/search.py` (to get tool request)

**Destroyed**: When the state is replaced with a new conversation turn

---

### ToolRequest Lifecycle

```
Creation
    |
    v
Extracted from PlannerDecision.tool_request
    |
    v
Passed to ToolManager.execute()
    |
    v
ToolManager looks up tool in registry
    |
    v
Tool.run() called with request.parameters
    |
    v
Request no longer needed after execution
    |
    v
Garbage collected
```

**Purpose**: Request object that tells the system which tool to run and with what parameters.

**Created by**: LLM as part of PlannerDecision

**Used by**: `app/tool_manager.py` (to execute tool)

**Destroyed**: After tool execution completes

---

### ToolResult Lifecycle

```
Creation
    |
    v
Tool.run() returns ToolResult
    |
    v
search_node adds to state
    |
    v
PromptBuilder reads from state
    |
    v
ToolManager.format() called
    |
    v
Tool.format_for_prompt() converts to string
    |
    v
String added to prompt context
    |
    v
Result no longer needed after prompt building
    |
    v
Garbage collected when state is replaced
```

**Purpose**: Standardized result object returned by all tools.

**Created by**: Individual tool implementations (e.g., DuckDuckGoSearchTool)

**Used by**:
- `app/nodes/search.py` (adds to state)
- `app/builders/prompt_builder.py` (formats for prompt)

**Destroyed**: When the state is replaced with a new conversation turn

---

### AgentState Lifecycle

```
Creation
    |
    v
main.py creates initial state
    {
        "messages": [HumanMessage]
    }
    |
    v
Passed to graph.invoke()
    |
    v
planner_node adds planner_decision
    |
    v
search_node adds tool_result
    |
    v
chat_node adds AIMessage to messages
    |
    v
graph returns final state
    |
    v
main.py extracts last message
    |
    v
State discarded (new state created next turn)
```

**Purpose**: Shared state object that travels through all graph nodes.

**Created by**: `main.py` at the start of each conversation turn

**Used by**: All nodes (planner, search, chat)

**Destroyed**: After each conversation turn (new state created for next turn)

---

### Conversation Lifecycle

```
Creation
    |
    v
main.py creates empty list
    |
    v
User input added as HumanMessage
    |
    v
AI response added as AIMessage
    |
    v
List grows with each turn
    |
    v
Conversation persists across turns
    |
    v
Cleared when user exits or restarts
```

**Purpose**: Maintains the history of the conversation.

**Created by**: `main.py` as a simple Python list

**Used by**: Passed to graph in state["messages"]

**Destroyed**: When the application exits or conversation is reset

---

## 10. Runtime Sequence Diagram

### Complete Runtime Sequence

```
User
    |
    | 1. Type "Latest AI news"
    v
main.py
    |
    | 2. Create HumanMessage
    v
main.py
    |
    | 3. Create state
    v
main.py
    |
    | 4. Load tools (ToolLoader.load_tools)
    v
ToolLoader
    |
    | 5. Register DuckDuckGoSearchTool
    v
ToolRegistry
    |
    | 6. Store tool
    v
ToolRegistry
    |
    | 7. Return to main.py
    v
main.py
    |
    | 8. Invoke graph
    v
graph (LangGraph)
    |
    | 9. Execute planner_node
    v
planner_node
    |
    | 10. Invoke planner_chain
    v
planner_chain
    |
    | 11. Combine prompt + LLM
    v
get_llm()
    |
    | 12. Return ChatOpenAI instance
    v
planner_chain
    |
    | 13. Call LLM
    v
OpenRouter API
    |
    | 14. Return PlannerDecision
    v
planner_chain
    |
    | 15. Return to planner_node
    v
planner_node
    |
    | 16. Add decision to state
    v
planner_node
    |
    | 17. Return to graph
    v
graph
    |
    | 18. Call planner_router
    v
planner_router
    |
    | 19. Check use_tool flag
    v
planner_router
    |
    | 20. Return "search"
    v
graph
    |
    | 21. Execute search_node
    v
search_node
    |
    | 22. Call ToolManager.execute
    v
ToolManager
    |
    | 23. Get tool from registry
    v
ToolRegistry
    |
    | 24. Return DuckDuckGoSearchTool
    v
ToolManager
    |
    | 25. Call tool.run()
    v
DuckDuckGoSearchTool
    |
    | 26. Search web via DDGS
    v
DuckDuckGo API
    |
    | 27. Return results
    v
DuckDuckGoSearchTool
    |
    | 28. Return ToolResult
    v
ToolManager
    |
    | 29. Return to search_node
    v
search_node
    |
    | 30. Add tool_result to state
    v
search_node
    |
    | 31. Return to graph
    v
graph
    |
    | 32. Execute chat_node
    v
chat_node
    |
    | 33. Call PromptBuilder.build
    v
PromptBuilder
    |
    | 34. Call ToolManager.format
    v
ToolManager
    |
    | 35. Call tool.format_for_prompt
    v
DuckDuckGoSearchTool
    |
    | 36. Format results as string
    v
DuckDuckGoSearchTool
    |
    | 37. Return formatted string
    v
ToolManager
    |
    | 38. Return to PromptBuilder
    v
PromptBuilder
    |
    | 39. Build prompt data
    v
PromptBuilder
    |
    | 40. Return to chat_node
    v
chat_node
    |
    | 41. Invoke chat_chain
    v
chat_chain
    |
    | 42. Combine prompt + LLM
    v
get_llm()
    |
    | 43. Return ChatOpenAI instance
    v
chat_chain
    |
    | 44. Call LLM with context
    v
OpenRouter API
    |
    | 45. Return AIMessage
    v
chat_chain
    |
    | 46. Return to chat_node
    v
chat_node
    |
    | 47. Add AIMessage to state
    v
chat_node
    |
    | 48. Return to graph
    v
graph
    |
    | 49. Reach END
    v
graph
    |
    | 50. Return final state
    v
main.py
    |
    | 51. Extract last message
    v
main.py
    |
    | 52. Display to user
    v
User
```

---

## 11. Beginner Walkthrough

### If I Clone This Repository Today, Where Should I Start Reading?

#### Recommended Reading Order

1. **main.py** (Start here)
   - Why: This is the entry point. It shows how the whole system starts.
   - What you'll learn: How the agent is initialized, how user input is handled, how the graph is invoked.

2. **app/graph.py** (Second)
   - Why: Shows the overall workflow structure.
   - What you'll learn: How nodes are connected, how the workflow flows, what the main components are.

3. **app/state.py** (Third)
   - Why: Understanding the state is crucial to understanding data flow.
   - What you'll learn: What data travels between nodes, what information is available at each step.

4. **app/schema.py** (Fourth)
   - Why: Defines all the data structures used in the system.
   - What you'll learn: What a PlannerDecision looks like, what a ToolResult contains, how data is structured.

5. **app/nodes/planner.py** (Fifth)
   - Why: The first node that executes. Shows how a node works.
   - What you'll learn: How nodes receive state, how they call chains, how they update state.

6. **app/chains/planner.py** (Sixth)
   - Why: Shows how to create an LLM chain.
   - What you'll learn: How prompts and LLMs are combined, how structured output works.

7. **app/prompts/planner.py** (Seventh)
   - Why: Shows how to guide the LLM's behavior.
   - What you'll learn: How to write system prompts, how to instruct the LLM.

8. **app/router.py** (Eighth)
   - Why: Shows how conditional routing works.
   - What you'll learn: How decisions lead to different paths, how the graph branches.

9. **app/nodes/search.py** (Ninth)
   - Why: Shows how tools are executed.
   - What you'll learn: How tool requests are processed, how ToolManager works.

10. **app/tool_manager.py** (Tenth)
    - Why: Central tool execution logic.
    - What you'll learn: How tools are looked up, how they're executed, how results are formatted.

11. **app/tools/base.py** (Eleventh)
    - Why: Shows the tool interface.
    - What you'll learn: What methods every tool must implement, how tools are designed.

12. **app/tools/registry.py** (Twelfth)
    - Why: Shows how tools are managed.
    - What you'll learn: How tools are stored, how they're retrieved, the registry pattern.

13. **app/tools/search_tool.py** (Thirteenth)
    - Why: Concrete tool implementation.
    - What you'll learn: How to implement a real tool, how to handle external APIs.

14. **app/tools/loader.py** (Fourteenth)
    - Why: Shows how tools are loaded at startup.
    - What you'll learn: How the system discovers and registers tools.

15. **app/nodes/chat.py** (Fifteenth)
    - Why: Shows how the final response is generated.
    - What you'll learn: How tool results are used, how the final response is created.

16. **app/builders/prompt_builder.py** (Sixteenth)
    - Why: Shows how prompt data is constructed.
    - What you'll learn: How to prepare data for the LLM, how to format tool results.

17. **app/chains/chat.py** (Seventeenth)
    - Why: Shows the chat chain.
    - What you'll learn: How the response chain differs from the planner chain.

18. **app/prompts/chat.py** (Eighteenth)
    - Why: Shows the chat system prompt.
    - What you'll learn: How to instruct the LLM to use tool context.

19. **app/llm.py** (Nineteenth)
    - Why: Shows LLM initialization.
    - What you'll learn: How to configure the LLM, how to use different providers.

20. **app/config.py** (Twentieth)
    - Why: Shows configuration management.
    - What you'll learn: How to use environment variables, how to provide defaults.

21. **app/enums.py** (Twenty-first)
    - Why: Shows type-safe constants.
    - What you'll learn: How to use enums for type safety.

### Why This Order?

This order follows the **execution flow** of the application:

1. Start with the entry point (main.py)
2. Understand the workflow structure (graph.py)
3. Understand the data that flows (state.py, schema.py)
4. Follow the execution through each node (planner → search → chat)
5. Understand the supporting systems (chains, prompts, tools)
6. Understand the infrastructure (llm, config, enums)

This approach lets you see the "big picture" first, then dive into details. You'll understand how pieces fit together before learning how each piece works internally.

---

## 12. Dependency Graph

### Forward Dependencies (Who Depends on Whom)

```
main.py
    |
    v
app/graph.py
    |
    +---> app/state.py
    |       |
    |       +---> app/schema.py
    |               |
    |               +---> app/enums.py
    |
    +---> app/nodes/planner.py
    |       |
    |       +---> app/chains/planner.py
    |               |
    |               +---> app/llm.py
    |               |       |
    |               |       +---> app/config.py
    |               |
    |               +---> app/prompts/planner.py
    |
    +---> app/nodes/search.py
    |       |
    |       +---> app/tool_manager.py
    |               |
    |               +---> app/tools/registry.py
    |                       |
    |                       +---> app/tools/base.py
    |                               |
    |                               +---> app/enums.py
    |                               +---> app/schema.py
    |
    +---> app/nodes/chat.py
    |       |
    |       +---> app/builders/prompt_builder.py
    |       |       |
    |       |       +---> app/tool_manager.py
    |       |
    |       +---> app/chains/chat.py
    |               |
    |               +---> app/llm.py
    |               |
    |               +---> app/prompts/chat.py
    |
    +---> app/router.py
            |
            +---> app/state.py
            +---> app/enums.py
```

### Reverse Dependencies (Who Is Used by Whom)

```
app/enums.py
    |
    +---> app/schema.py
    |       |
    |       +---> app/state.py
    |               |
    |               +---> app/router.py
    |               +---> app/nodes/*.py
    |
    +---> app/tools/base.py
            |
            +---> app/tools/registry.py
                    |
                    +---> app/tool_manager.py
                            |
                            +---> app/nodes/search.py
                            +---> app/builders/prompt_builder.py

app/config.py
    |
    +---> app/llm.py
            |
            +---> app/chains/planner.py
            +---> app/chains/chat.py
                    |
                    +---> app/nodes/planner.py
                    +---> app/nodes/chat.py

app/schema.py
    |
    +---> app/state.py
    +---> app/tools/base.py

app/state.py
    |
    +---> app/graph.py
    +---> app/nodes/*.py
    +---> app/router.py
    +---> app/builders/prompt_builder.py
```

### Dependency Levels

**Level 0 (No dependencies)**:
- `app/enums.py`
- `app/config.py`

**Level 1 (Depends on Level 0)**:
- `app/schema.py` (depends on enums)
- `app/llm.py` (depends on config)

**Level 2 (Depends on Level 0-1)**:
- `app/tools/base.py` (depends on enums, schema)
- `app/prompts/planner.py` (no dependencies, but conceptually level 2)
- `app/prompts/chat.py` (no dependencies, but conceptually level 2)

**Level 3 (Depends on Level 0-2)**:
- `app/tools/registry.py` (depends on base, enums)
- `app/chains/planner.py` (depends on llm, prompts, schema)
- `app/chains/chat.py` (depends on llm, prompts)

**Level 4 (Depends on Level 0-3)**:
- `app/tool_manager.py` (depends on registry, schema)
- `app/state.py` (depends on schema)

**Level 5 (Depends on Level 0-4)**:
- `app/tools/search_tool.py` (depends on base, enums, schema)
- `app/tools/loader.py` (depends on registry, search_tool)
- `app/builders/prompt_builder.py` (depends on state, tool_manager)
- `app/router.py` (depends on state, enums)

**Level 6 (Depends on Level 0-5)**:
- `app/nodes/planner.py` (depends on chains, state)
- `app/nodes/search.py` (depends on state, tool_manager)
- `app/nodes/chat.py` (depends on builders, chains, state)

**Level 7 (Depends on Level 0-6)**:
- `app/graph.py` (depends on state, nodes, router)

**Level 8 (Depends on Level 0-7)**:
- `main.py` (depends on graph, tools/loader)

---

## 13. Extension Guide

### How to Add a New Tool

Let's say you want to add a **Calculator Tool** that can perform mathematical calculations.

#### Step 1: Add Tool Name to Enum

**File**: `app/enums.py`

Add the new tool name to the `ToolName` enum:

```python
class ToolName(str, Enum):
    SEARCH = "search"
    CALCULATOR = "calculator"  # Add this line
    PYTHON = "python"
    WEB_BROWSER = "web_browser"
    # ... existing tools
```

**Why**: The enum provides type-safe tool names throughout the system. This prevents typos and makes refactoring easier.

---

#### Step 2: Create the Tool Implementation

**File**: Create `app/tools/calculator_tool.py`

```python
from app.enums import ToolName
from app.schema import ToolResult
from app.tools.base import BaseTool

class CalculatorTool(BaseTool):
    """
    Perform mathematical calculations.
    """
    
    def __init__(self):
        super().__init__(
            name=ToolName.CALCULATOR,
            description="Perform mathematical calculations"
        )
    
    def run(self, expression: str) -> ToolResult:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: A mathematical expression like "2 + 2 * 3"
        """
        try:
            # Use eval for simplicity (in production, use a safer alternative)
            result = eval(expression)
            
            return ToolResult(
                success=True,
                tool_name=self.name,
                content={"expression": expression, "result": result}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                tool_name=self.name,
                content=None,
                error=str(e)
            )
    
    def format_for_prompt(self, result: ToolResult) -> str:
        """
        Format the calculation result for the LLM prompt.
        """
        if not result.success or result.content is None:
            return ""
        
        content = result.content
        return f"Calculation: {content['expression']} = {content['result']}"
```

**Why**: This implements the actual tool logic. It inherits from BaseTool, which enforces the interface. The `run()` method does the work, and `format_for_prompt()` converts the result to text for the LLM.

---

#### Step 3: Register the Tool

**File**: `app/tools/loader.py`

Import and register your new tool:

```python
from app.tools.registry import tool_registry
from app.tools.search_tool import DuckDuckGoSearchTool
from app.tools.calculator_tool import CalculatorTool  # Add this import

class ToolLoader:
    """
    Loads and registers all tools.
    """
    
    @staticmethod
    def load_tools() -> None:
        tool_registry.register(DuckDuckGoSearchTool())
        tool_registry.register(CalculatorTool())  # Add this line
```

**Why**: The loader is responsible for discovering and registering all tools at startup. By adding it here, your tool will be available when the application starts.

---

#### Step 4: Update the Planner Prompt

**File**: `app/prompts/planner.py`

Add information about your new tool:

```python
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the planning component of an AI Agent.

Your responsibility is ONLY to decide whether a tool is required.

Available tools:

1. search
   Use for:
   - latest news
   - current events
   - real-time information
   - internet searches

2. calculator  # Add this section
   Use for:
   - mathematical calculations
   - arithmetic operations
   - numerical computations

If the question can be answered from general knowledge,
do NOT use a tool.

Return your answer using the required structured format.
"""
        ),
        ("placeholder", "{messages}")
    ]
)
```

**Why**: The planner needs to know about your tool so it can decide when to use it. Without this information, the planner will never choose your tool.

---

#### Step 5: Add a Node for Your Tool (If Needed)

**File**: `app/nodes/calculator.py` (create new file)

```python
from app.state import AgentState
from app.tool_manager import ToolManager

def calculator_node(state: AgentState) -> AgentState:
    """
    Calculator node.
    
    Executes the calculator tool and stores the result.
    """
    decision = state["planner_decision"]
    
    if decision.tool_request is None:
        return state
    
    tool_result = ToolManager.execute(decision.tool_request)
    
    return {
        **state,
        "tool_result": tool_result
    }
```

**Why**: Each tool needs a node that executes it. The node extracts the tool request from the state, executes it via ToolManager, and stores the result.

---

#### Step 6: Register the Node in the Graph

**File**: `app/graph.py`

Import and add your node:

```python
from app.nodes.planner import planner_node
from app.nodes.chat import chat_node
from app.nodes.search import search_node
from app.nodes.calculator import calculator_node  # Add this import

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("calculator", calculator_node)  # Add this line
builder.add_node("chat", chat_node)

# ... rest of the graph setup
```

**Why**: The graph needs to know about your node so it can execute it when the router directs to it.

---

#### Step 7: Test Your Tool

Create a test file or run the agent and try:

```
You: What is 12345 * 67890?
```

The planner should recognize this needs the calculator, route to the calculator node, execute the calculation, and the chat node should use the result to answer.

---

### Summary of Extension Steps

1. **Add enum**: Type-safe constant for the tool name
2. **Implement tool**: Create the actual tool class with run() and format_for_prompt()
3. **Register tool**: Add to loader so it's available at startup
4. **Update prompt**: Tell the planner about the new tool
5. **Create node**: Add a node to execute the tool
6. **Register node**: Add the node to the graph
7. **Test**: Verify it works end-to-end

This pattern ensures that adding a new tool doesn't require modifying core logic. You're extending the system through plugins.

---

## 14. Design Principles

### Single Responsibility Principle

**Definition**: Each class or module should have one reason to change.

**How this project follows it**:

- **Planner Node**: Only decides whether to use a tool. It doesn't execute tools or generate responses.
- **Search Node**: Only executes tools. It doesn't decide which tool or generate responses.
- **Chat Node**: Only generates responses. It doesn't decide or execute.
- **ToolManager**: Only manages tool execution. It doesn't know about the graph or prompts.
- **PromptBuilder**: Only builds prompt data. It doesn't call the LLM.
- **ToolRegistry**: Only stores tools. It doesn't execute them.

**Benefit**: If you need to change how tools are executed, you only modify ToolManager. If you need to change how responses are generated, you only modify ChatNode. Changes are isolated.

---

### Open/Closed Principle

**Definition**: Software entities should be open for extension but closed for modification.

**How this project follows it**:

- **BaseTool**: Defines an interface. New tools can be added by inheriting from BaseTool without modifying BaseTool.
- **ToolRegistry**: Accepts any BaseTool implementation. New tools can be registered without changing the registry code.
- **ToolLoader**: Can be extended to load more tools without changing the loading logic.
- **Graph Nodes**: New nodes can be added without modifying existing nodes.

**Example**: When we added the Calculator tool in the extension guide, we didn't modify any existing tool code. We just added a new file and registered it.

**Benefit**: The system grows through addition, not modification. This reduces the risk of breaking existing functionality.

---

### Dependency Inversion Principle

**Definition**: Depend on abstractions, not concretions.

**How this project follows it**:

- **ToolManager depends on BaseTool (abstract)**, not DuckDuckGoSearchTool (concrete).
- **ToolRegistry stores BaseTool references**, not specific tool classes.
- **Nodes depend on AgentState (abstract type)**, not specific implementations.
- **Chains depend on prompt templates (abstractions)**, not hardcoded strings.

**Example**: In `tool_manager.py`:

```python
tool = tool_registry.get(request.tool_name)
return tool.run(**request.parameters)
```

ToolManager doesn't know which tool it's calling. It just knows the tool has a `run()` method because it inherits from BaseTool.

**Benefit**: You can swap implementations without changing dependent code. For example, you could replace DuckDuckGoSearchTool with GoogleSearchTool without changing ToolManager.

---

### Abstraction

**Definition**: Hide complex implementation details behind simple interfaces.

**How this project follows it**:

- **BaseTool**: Hides the complexity of individual tools behind a simple interface with two methods.
- **ToolManager**: Hides the complexity of tool lookup, execution, and formatting behind simple methods.
- **Graph**: Hides the complexity of workflow execution behind a simple `invoke()` call.
- **Chains**: Hides the complexity of prompt construction and LLM calling behind the pipe operator.

**Example**: When `search_node` calls `ToolManager.execute()`, it doesn't need to know:
- How the tool is looked up in the registry
- How the tool's `run()` method works internally
- How errors are handled
- How the result is structured

It just knows: "I give you a request, you give me a result."

**Benefit**: Complexity is managed locally. Each component only needs to understand its own complexity, not the entire system.

---

### Composition

**Definition**: Combine simple objects to build complex systems.

**How this project follows it**:

- **Graph**: Composed of nodes, edges, and state
- **Nodes**: Composed of chains and state manipulation
- **Chains**: Composed of prompts and LLMs
- **Prompts**: Composed of system messages and placeholders
- **Tool System**: Composed of registry, manager, base class, and implementations

**Example**: The chat node is composed of:
- PromptBuilder (builds data)
- ChatChain (processes data)
- State manipulation (updates data)

None of these components know about each other's internals. They just work together through well-defined interfaces.

**Benefit**: The system is modular. You can swap out PromptBuilder, ChatChain, or the state structure without rewriting everything.

---

### Plugin Architecture

**Definition**: Allow functionality to be added through plugins without modifying core code.

**How this project follows it**:

- **Tools are plugins**: New tools can be added by:
  1. Creating a new file
  2. Inheriting from BaseTool
  3. Registering in ToolLoader
- **No core changes needed**: Adding a tool doesn't require modifying graph.py, nodes, or chains (except adding the node itself).
- **Dynamic loading**: Tools are loaded at runtime through the registry.

**Example**: The search tool is a plugin. If you want to add a Wikipedia tool, you:
1. Create `wikipedia_tool.py`
2. Inherit from BaseTool
3. Add to ToolLoader
4. Add to planner prompt
5. Create a node
6. Add to graph

You never modify the existing search tool or core agent logic.

**Benefit**: The system is extensible. New capabilities can be added without risking existing functionality.

---

### Strategy Pattern

**Definition**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

**How this project follows it**:

- **Tools are strategies**: Each tool is a different strategy for getting information.
- **Tool execution**: The system can use any tool strategy through the common BaseTool interface.
- **Routing**: The router decides which strategy (tool) to use based on the planner's decision.

**Example**: The planner might decide:
- Use SEARCH strategy for "latest news"
- Use CALCULATOR strategy for "2 + 2"
- Use WIKIPEDIA strategy for "history of Rome"

Each strategy is interchangeable through the ToolManager.

**Benefit**: The decision of which strategy to use is separated from the execution of the strategy.

---

### Registry Pattern

**Definition**: Provide a central location for registering and looking up objects.

**How this project follows it**:

- **ToolRegistry**: Central registry for all tools.
- **Registration**: Tools register themselves at startup.
- **Lookup**: Components request tools by name from the registry.
- **Decoupling**: Components don't need to know where tools come from.

**Example**: When ToolManager needs a tool:
```python
tool = tool_registry.get(request.tool_name)
```

It doesn't import the tool directly. It asks the registry.

**Benefit**: Loose coupling. Components don't need to know about specific tool implementations.

---

## 15. Architecture Summary

### Complete Project Architecture

```
User
    |
    v
main.py (Entry Point)
    |
    +---> ToolLoader.load_tools()
    |       |
    |       v
    |   ToolRegistry
    |       |
    |       +---> DuckDuckGoSearchTool
    |       +---> [Future tools]
    |
    v
Conversation Loop
    |
    v
Create HumanMessage
    |
    v
Create AgentState
    |
    v
graph.invoke(state)
    |
    v
LangGraph Workflow
    |
    v
START
    |
    v
planner_node
    |
    +---> planner_chain
    |       |
    |       +---> planner_prompt
    |       |
    |       +---> get_llm()
    |               |
    |               +---> Settings (config)
    |               |
    |               v
    |           ChatOpenAI
    |
    v
PlannerDecision
    |
    v
planner_router
    |
    +---> [Conditional Routing]
    |
    +---+----------------+
        |                |
        v                v
    use_tool=true     use_tool=false
        |                |
        v                |
    search_node         |
        |                |
        +---> ToolManager.execute()
        |       |
        |       +---> ToolRegistry.get()
        |       |
        |       v
        |   DuckDuckGoSearchTool.run()
        |       |
        |       +---> DDGS API
        |       |
        |       v
        |   ToolResult
        |
        v
    tool_result added to state
        |
        +----------------+
        |                |
        v                v
    chat_node <---------+
    |
    +---> PromptBuilder.build()
    |       |
    |       +---> ToolManager.format()
    |               |
    |               +---> DuckDuckGoSearchTool.format_for_prompt()
    |
    v
prompt_data
    |
    v
chat_chain
    |
    +---> chat_prompt
    |
    +---> get_llm()
    |
    v
ChatOpenAI
    |
    v
AIMessage
    |
    v
Add to state.messages
    |
    v
END
    |
    v
Return state to main.py
    |
    v
Extract last message
    |
    v
Display to user
    |
    v
User
```

---

### Key Architectural Components

#### 1. Entry Layer
- **main.py**: Application bootstrap and user interaction

#### 2. Workflow Layer
- **graph.py**: Defines the workflow structure
- **router.py**: Controls workflow branching

#### 3. Execution Layer
- **nodes/**: Individual workflow steps
- **chains/**: LLM interaction chains
- **prompts/**: AI behavior definitions

#### 4. Data Layer
- **state.py**: Shared state definition
- **schema.py**: Data models
- **enums.py**: Type-safe constants

#### 5. Tool Layer
- **tool_manager.py**: Tool execution coordinator
- **tools/base.py**: Tool interface
- **tools/registry.py**: Tool storage
- **tools/loader.py**: Tool initialization
- **tools/search_tool.py**: Concrete tool implementation

#### 6. Infrastructure Layer
- **llm.py**: LLM initialization
- **config.py**: Configuration management
- **builders/**: Data construction helpers

---

### Data Flow Summary

```
User Input
    |
    v
HumanMessage
    |
    v
AgentState
    |
    v
PlannerDecision
    |
    v
ToolRequest (if needed)
    |
    v
ToolResult (if tool used)
    |
    v
Prompt Data
    |
    v
AIMessage
    |
    v
User Output
```

---

### Design Patterns Used

1. **Registry Pattern**: ToolRegistry for managing tools
2. **Strategy Pattern**: Different tools as interchangeable strategies
3. **Plugin Architecture**: Tools as plugins
4. **Template Method**: BaseTool defines the algorithm structure
5. **Builder Pattern**: PromptBuilder constructs complex objects
6. **Chain of Responsibility**: Graph nodes form a chain
7. **Facade Pattern**: ToolManager hides tool complexity
8. **Factory Pattern**: ToolLoader creates tool instances

---

### Extension Points

To extend the system, you can:

1. **Add new tools**: Inherit from BaseTool, register in ToolLoader
2. **Add new nodes**: Create node function, register in graph
3. **Add new chains**: Create chain, use in nodes
4. **Modify prompts**: Edit prompt templates to change AI behavior
5. **Add new data models**: Add to schema.py
6. **Change routing**: Modify router.py for new decision logic
7. **Swap LLM provider**: Modify llm.py and config.py

---

# Project Cheat Sheet

## Quick Reference

### Purpose
AI Agent that decides when to use external tools (like web search) vs. answering from knowledge.

### Technology Stack
- **Framework**: LangGraph (workflow orchestration)
- **LLM**: OpenRouter API
- **Language**: Python
- **Search**: DuckDuckGo
- **Data Validation**: Pydantic

### Entry Point
`main.py` - Run this to start the agent

### Core Workflow
```
User Input → Planner → [Tool? → Tool Execution] → Chat → Response
```

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point, conversation loop |
| `app/graph.py` | Workflow definition |
| `app/state.py` | Shared state structure |
| `app/schema.py` | Data models |
| `app/nodes/planner.py` | Decision making |
| `app/nodes/search.py` | Tool execution |
| `app/nodes/chat.py` | Response generation |
| `app/tool_manager.py` | Tool coordination |
| `app/tools/base.py` | Tool interface |
| `app/tools/search_tool.py` | Web search implementation |

### Key Classes

| Class | Purpose |
|-------|---------|
| `AgentState` | Shared state between nodes |
| `PlannerDecision` | Planner's decision object |
| `ToolRequest` | Request to execute a tool |
| `ToolResult` | Result from tool execution |
| `BaseTool` | Interface all tools must implement |
| `ToolRegistry` | Central tool storage |
| `ToolManager` | Tool execution coordinator |

### Execution Flow (Simple)

1. User types question
2. Planner decides: tool or no tool?
3. If tool: execute tool, get results
4. Chat node uses results (if any) to generate response
5. Response shown to user

### Adding a New Tool

1. Add to `ToolName` enum in `app/enums.py`
2. Create tool class inheriting from `BaseTool`
3. Register in `app/tools/loader.py`
4. Update `app/prompts/planner.py`
5. Create node in `app/nodes/`
6. Add node to `app/graph.py`

### Configuration

Edit `.env` file:
- `OPENROUTER_API_KEY`: Your API key
- `MODEL_NAME`: Model to use
- `TEMPERATURE`: LLM creativity (0-1)
- `MAX_TOKENS`: Response length limit

### Dependencies

Install required packages:
```
langgraph
langchain
langchain-openai
langchain-core
pydantic
python-dotenv
ddgs
```

### Architecture Principles

- **Single Responsibility**: Each component has one job
- **Open/Closed**: Extend through plugins, don't modify core
- **Dependency Inversion**: Depend on abstractions
- **Plugin Architecture**: Tools are plugins
- **Registry Pattern**: Central tool management

### Testing

Run tests:
```
python test_planner.py
python test_search_node.py
```

### Common Modifications

| Goal | What to Change |
|------|----------------|
| Change AI behavior | Edit `app/prompts/` |
| Add new tool | See "Adding a New Tool" above |
| Change LLM | Edit `app/config.py` |
| Modify workflow | Edit `app/graph.py` |
| Change routing logic | Edit `app/router.py` |

---

## End of Documentation
