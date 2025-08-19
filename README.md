# StoryWeaverAI

A Simple AI-powered story generation system that creates original short stories using LangGraph agents and Azure OpenAI, stores them in Notion as structured entries, and delivers them via Telegram using n8n automation.

## 🌟 Features

- **AI Story Generation**: Uses LangGraph agents with Azure OpenAI to create original, creative short stories
- **Structured Notion Storage**: Automatically saves stories to Notion with organized metadata (title, setting, characters, conflict, resolution)
- **Telegram Delivery**: Sends stories to users via Telegram in beautiful multi-part Markdown format
- **Multi-Agent Workflow**: Orchestrates multiple AI agents for idea generation, character development, plot creation, and story resolution
- **Automated Pipeline**: Complete automation from story generation to delivery using n8n workflows

## 🏗️ Architecture

```
User Input → LangGraph Agents → Azure OpenAI → Story Generation → Notion Storage → n8n → Telegram Delivery
```

### Core Components

- **Idea Generator Agent**: Creates creative story concepts and themes
- **Setting Agent**: Develops rich, immersive story environments
- **Character Agent**: Crafts compelling characters with motivations and traits
- **Conflict Agent**: Establishes central tensions and plot drivers
- **Resolution Agent**: Writes satisfying story conclusions
- **Notion Integration**: Stores structured story data with metadata
- **n8n Automation**: Orchestrates Telegram delivery workflow

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.11+**: Main application language
- **LangGraph**: Multi-agent workflow orchestration
- **Azure OpenAI**: GPT-4 powered story generation
- **Notion SDK**: Database integration and story storage
- **python-dotenv**: Environment configuration

### Automation & Delivery
- **n8n**: Workflow automation platform
- **Telegram Bot API**: Story delivery to users
- **Markdown**: Rich text formatting for stories

### Development Tools
- **Virtual Environment**: Isolated Python dependencies
- **Requirements.txt**: Dependency management
- **Environment Variables**: Secure configuration management

## 📋 Prerequisites

- Python 3.11 or higher
- Azure OpenAI account with API access
- Notion workspace with database
- Telegram Bot token
- n8n instance (self-hosted or cloud)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/storyweaver-ai.git
cd storyweaver-ai
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration
OPENAI_API_TYPE=azure
OPENAI_API_KEY=your_azure_openai_api_key
OPENAI_API_BASE=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2025-01-01-preview
OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Notion Integration
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id

# Telegram Bot (for n8n integration)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

## 🔧 Setup Instructions

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in Azure Portal
2. Deploy a GPT-4 model (recommended: gpt-4o)
3. Copy your API key, endpoint, and deployment name
4. Add to your `.env` file

### Notion Database Setup
1. Create a new database in Notion
2. Add the following properties:
   - **Title** (Title type) - Story title
   - **Status** (Select type) - Generated, Draft, Published
   - **Setting** (Text type) - Story setting
   - **Characters** (Text type) - Character descriptions
   - **Conflict** (Text type) - Central conflict
   - **Resolution** (Text type) - Story resolution
   - **Ideas** (Text type) - Generated story ideas
3. Create a Notion integration at https://www.notion.so/my-integrations
4. Share your database with the integration
5. Copy the integration token and database ID

### n8n Workflow Setup
1. Install n8n (self-hosted or use n8n.cloud)
2. Create a workflow that:
   - Monitors the Notion database for new entries
   - Formats stories into Markdown
   - Sends to Telegram via Bot API
3. Configure Telegram Bot token in n8n

## 🎯 Usage

### Run Story Generation
```bash
python main.py
```

The application will:
1. Prompt for a story theme or concept
2. Generate creative story ideas using AI agents
3. Develop setting, characters, conflict, and resolution
4. Save the complete story to Notion
5. Trigger n8n workflow for Telegram delivery

### Test Integration
```bash
python test_integration.py
```

This runs comprehensive tests for:
- Azure OpenAI connection
- Notion database integration
- LangGraph workflow
- Story generation pipeline

### Setup Verification
```bash
python setup_notion.py
```

Verifies Notion integration and provides setup guidance.

## 📁 Project Structure

```
storyweaver-ai/
├── agents/                 # LangGraph agent modules
│   ├── idea_generator_agent.py
│   ├── character_agent.py
│   ├── editor_agent.py
│   └── storyteller.py
├── utils/                  # Utility modules
│   ├── notion_client.py    # Notion integration
│   └── prompts.py         # AI prompt templates
├── main.py                # Main application entry point
├── setup_notion.py        # Notion setup verification
├── test_integration.py    # Integration testing
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
└── README.md             # This file
```

## 🔄 Workflow Process

1. **User Input**: User provides a story theme or concept
2. **Idea Generation**: AI generates multiple creative story ideas
3. **Setting Development**: Creates immersive story environment
4. **Character Creation**: Develops compelling characters with motivations
5. **Conflict Establishment**: Establishes central plot tension
6. **Resolution Writing**: Crafts satisfying story conclusion
7. **Notion Storage**: Saves structured story data to database
8. **n8n Trigger**: Automatically triggers Telegram delivery workflow
9. **Telegram Delivery**: Sends formatted story to user

## 🧪 Testing

### Run All Tests
```bash
python test_integration.py
```

### Test Individual Components
```bash
# Test Notion connection
python setup_notion.py

# Test token validity
python test_notion_token.py
```

## 🔒 Security

- All API keys stored in environment variables
- No hardcoded credentials in source code
- Secure token management for Notion and Telegram
- Azure OpenAI API key rotation support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- **LangGraph**: For multi-agent workflow orchestration
- **Azure OpenAI**: For powerful AI story generation
- **Notion**: For structured data storage
- **n8n**: For workflow automation
- **Telegram**: For story delivery platform


**StoryWeaverAI** - Where AI meets creativity, one story at a time. 📚✨ 