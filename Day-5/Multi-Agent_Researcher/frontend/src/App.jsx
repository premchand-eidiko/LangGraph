import React, { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

function App() {
  const [threadId, setThreadId] = useState("")
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true'
  })
  const [error, setError] = useState("")
  const [workflowSteps, setWorkflowSteps] = useState([])
  const [currentStep, setCurrentStep] = useState("")
  const chatEndRef = useRef(null)
  const abortControllerRef = useRef(null)

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode)
    document.body.className = darkMode ? 'dark-mode' : 'light-mode'
  }, [darkMode])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const generateNewThreadId = () => {
    return `research-${Date.now()}`
  }

  const handleNewChat = () => {
    const newId = generateNewThreadId()
    setThreadId(newId)
    setMessages([])
    setQuestion("")
    setError("")
    setWorkflowSteps([])
    setCurrentStep("")
  }

  const handleSend = async () => {
    if (!threadId.trim()) {
      setError("Please enter a Thread ID.")
      return
    }
    if (!question.trim()) {
      return
    }
    if (loading) {
      return
    }

    setError("")
    const userMessage = { role: "user", content: question }
    const assistantMessage = { role: "assistant", content: "" }
    
    setMessages(prev => [...prev, userMessage, assistantMessage])
    setQuestion("")
    setLoading(true)
    setWorkflowSteps([])
    setCurrentStep("")

    abortControllerRef.current = new AbortController()

    // Start orchestration stream
    const orchestrationController = new AbortController()
    const orchestrationSignal = abortControllerRef.current.signal

    const orchestrationPromise = (async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/research/orchestration-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            thread_id: threadId,
            query: userMessage.content
          }),
          signal: orchestrationSignal
        })

        if (!response.ok) {
          throw new Error(`Orchestration stream error! status: ${response.status}`)
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value, { stream: true })
          const step = chunk.trim()
          if (step) {
            setCurrentStep(step)
            setWorkflowSteps(prev => {
              if (!prev.includes(step)) {
                return [...prev, step]
              }
              return prev
            })
          }
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Orchestration stream error:', err)
        }
      }
    })()

    // Start token stream for final report
    try {
      const response = await fetch(`${API_BASE_URL}/api/research/token-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          thread_id: threadId,
          query: userMessage.content
        }),
        signal: abortControllerRef.current.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        setMessages(prev => {
          const newMessages = [...prev]
          const lastAssistantIndex = newMessages.length - 1
          newMessages[lastAssistantIndex] = {
            ...newMessages[lastAssistantIndex],
            content: newMessages[lastAssistantIndex].content + chunk
          }
          return newMessages
        })
      }

    } catch (err) {
      if (err.name === 'AbortError') {
        console.log('Stream was stopped by user')
      } else {
        let errorMessage = "Unable to connect to the research server."
        if (err.message && err.message.includes('429')) {
          errorMessage = "Rate limit reached. Please wait a few minutes and try again."
        }
        setError(errorMessage)
        console.error('Error:', err)
      }
    } finally {
      orchestrationController.abort()
      await orchestrationPromise
      setLoading(false)
      abortControllerRef.current = null
      setCurrentStep("")
    }
  }

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleInputChange = (e) => {
    setQuestion(e.target.value)
    // Auto-resize textarea
    const textarea = e.target
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <div className="container">
        <header className="header">
          <div className="header-content">
            <h1 className="title">Multi-Agent Research Assistant</h1>
            <p className="subtitle">AI-powered research using collaborative agents</p>
          </div>
          <button 
            className="theme-toggle"
            onClick={toggleDarkMode}
            aria-label="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </header>

        <div className="thread-section">
          <label className="thread-label">Thread ID</label>
          <div className="thread-input-group">
            <input
              type="text"
              className="thread-input"
              value={threadId}
              onChange={(e) => setThreadId(e.target.value)}
              placeholder="research-001"
            />
            <button 
              className="new-chat-btn"
              onClick={handleNewChat}
            >
              New Chat
            </button>
          </div>
        </div>

        {(workflowSteps.length > 0 || currentStep) && (
          <div className="workflow-section">
            <div className="workflow-header">
              <h3 className="workflow-title">Research Workflow</h3>
              {currentStep && (
                <div className="current-step">
                  <span className="pulse"></span>
                  {currentStep}
                </div>
              )}
            </div>
            <div className="workflow-steps">
              {workflowSteps.map((step, index) => (
                <div key={index} className="workflow-step">
                  <div className="step-marker">
                    <div className="step-dot"></div>
                    {index < workflowSteps.length - 1 && <div className="step-line"></div>}
                  </div>
                  <div className="step-content">{step}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="chat-container">
          <div className="messages">
            {messages.length === 0 && (
              <div className="empty-state">
                <p>Start a research conversation by entering a question.</p>
              </div>
            )}
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-role">
                  {message.role === 'user' ? 'User' : 'Assistant'}
                </div>
                <div className="message-content">
                  {message.role === 'assistant' ? (
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="input-section">
            <textarea
              className="question-input"
              value={question}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask your research question..."
              disabled={loading}
              rows={1}
            />
            <button
              className="send-btn"
              onClick={loading ? handleStop : handleSend}
              disabled={!question.trim() || !threadId.trim()}
            >
              {loading ? 'Stop' : 'Send'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
