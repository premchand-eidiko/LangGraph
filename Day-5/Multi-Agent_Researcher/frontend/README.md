# Multi-Agent Research Assistant - Frontend

A simple React frontend for the Multi-Agent Research Assistant backend.

## Features

- Clean, modern chat interface
- Real-time streaming of research responses
- Thread ID management for conversation sessions
- Dark/Light mode toggle
- Responsive design
- Markdown rendering for assistant responses

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure the backend URL:
```bash
cp .env.example .env
# Edit .env if your backend is not at http://localhost:8000
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:3000`

## Usage

1. Enter a Thread ID (or click "New Chat" to generate one)
2. Type your research question
3. Click Send or press Enter
4. Watch the research response stream in real-time
5. Ask follow-up questions using the same Thread ID
6. Click "New Chat" to start a fresh conversation

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx       # Main application component
│   ├── main.jsx      # React entry point
│   └── App.css       # Application styles
├── .env              # Environment variables (not committed)
├── .env.example      # Environment variables template
├── index.html        # HTML entry point
├── package.json      # Dependencies and scripts
└── README.md         # This file
```

## API

The frontend connects to the FastAPI backend at:

- Streaming endpoint: `POST /api/research/token-stream`

## Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist/` directory.
