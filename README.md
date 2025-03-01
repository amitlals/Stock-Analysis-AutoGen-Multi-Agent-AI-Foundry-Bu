# 📈 Stock Analysis Multi-Agent System | Build using Autogen v0.4, Azure AI agent Services, Azure AI Foundry, AOAI

> 🤖 AI-powered stock analysis application built with Python, AutoGen multi-agent architecture, and Gradio UI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![AutoGen](https://img.shields.io/badge/AutoGen-Multi--Agent-orange) ![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)

## ✨ Features

- 🔐 **Secure Login** - Authentication system protects application access
- 🔄 **Dual API Sources** - Alpha Vantage API with automatic failover to Yahoo Finance
- 📊 **Technical Analysis** - Comprehensive metrics including:
  - Moving averages (50-day, 200-day)
  - Price trends and momentum indicators
  - Volatility measurements
  - 6-month and monthly returns
- 🧠 **AI-Powered Recommendations** - Get BUY/HOLD/SELL guidance based on technical indicators
- 📧 **Email Reports** - Send beautifully formatted HTML analysis reports via Azure Logic Apps
- 🤖 **Multi-Agent Architecture** - Leverages specialized AI agents for different analytical tasks

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Stock-Analysis-AutoGen-Multi-Agent-Azure.git
   cd Stock-Analysis-AutoGen-Multi-Agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your API keys and configuration settings.

## 🚀 Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:7860
   ```

3. Log in with your credentials.

4. Enter a stock symbol (e.g., AAPL, MSFT) and click "Analyze" to get AI-powered insights.

## 🔍 Project Structure

```
├── agents/                  # AutoGen multi-agent system components
│   ├── __init__.py
│   ├── analyst_agent.py     # Technical analysis agent
│   ├── data_agent.py        # Stock data retrieval agent
│   ├── planner_agent.py     # Coordinates the analysis workflow
│   └── recommender_agent.py # Generates investment recommendations
├── assets/                  # Static assets for UI
├── data/                    # Cached data and analysis results
├── ui/                      # Gradio UI components
│   ├── __init__.py
│   ├── app.py              # Main UI definition
│   └── components/         # Reusable UI components
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── api_handler.py      # API integration with fallback
│   ├── auth.py             # Authentication logic
│   ├── email_sender.py     # Email report functionality
│   └── technical.py        # Technical analysis functions
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── LICENSE                  # Project license
├── main.py                  # Application entry point
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## 🔑 API Keys

This application requires the following API keys:

1. **Alpha Vantage API** - Primary source for stock data
   - Get a free API key at: https://www.alphavantage.co/support/#api-key

2. **Azure OpenAI Service** - Powers the AI agents
   - Set up through Azure AI services: https://azure.microsoft.com/en-us/products/ai-services/openai-service

3. **Azure Logic Apps** (optional) - For email delivery
   - Configure through Azure portal: https://portal.azure.com

## 💌 Email Reports with LogicApps 

The system can send detailed stock analysis reports via email using Azure Logic Apps:

1. Create an HTTP-triggered Logic App in Azure
2. Add the Logic App URL to your `.env` file
3. Use the "Send Email" option in the application UI

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent framework
- [Gradio](https://gradio.app/) - UI framework
- [Alpha Vantage](https://www.alphavantage.co/) - Stock data API
- [Yahoo Finance](https://finance.yahoo.com/) - Backup stock data source
