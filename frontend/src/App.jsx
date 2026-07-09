import ReactMarkdown from 'react-markdown'
import { useState } from 'react'
import Typewriter from './Typewriter';

function App() {
  // 1. React State: Memory to hold our variables
  const [githubUrl, setGithubUrl] = useState("")
  const [question, setQuestion] = useState("")
  const [chatHistory, setChatHistory] = useState([
    { sender: "ai", text: "Hello! Paste a GitHub repository link in the sidebar, click Analyze, and then ask me anything about the codebase." }
  ])
  
  // Loading states for our buttons
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isAsking, setIsAsking] = useState(false)

  // 2. Function to handle the GitHub URL submission
  const handleAnalyzeRepo = async () => {
    if (!githubUrl) return
    
    setIsAnalyzing(true)
    try {
      const response = await fetch("https://ai-repo-analyzer-o0zo.onrender.com/process-github-repo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ github_url: githubUrl })
      })
      
      if (response.ok) {
        setChatHistory(prev => [...prev, { sender: "ai", text: "✅ Repository successfully analyzed and indexed! What would you like to know about it?" }])
      } else {
        setChatHistory(prev => [...prev, { sender: "ai", text: "❌ Error analyzing repository. Please check the URL and your backend terminal." }])
      }
    } catch (error) {
      setChatHistory(prev => [...prev, { sender: "ai", text: "❌ Connection error. Is your FastAPI server running?" }])
    }
    setIsAnalyzing(false)
  }

  // 3. Function to handle asking a question
  const handleSendMessage = async () => {
    if (!question) return

    // Add user's question to the chat immediately
    const userMessage = { sender: "human", text: question }
    setChatHistory(prev => [...prev, userMessage])
    setQuestion("") // clear the input box
    setIsAsking(true)

    try {
      const response = await fetch("https://ai-repo-analyzer-o0zo.onrender.com/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage.text })
      })
      
      const data = await response.json()
      
      // Add AI's response to the chat
      if (response.ok) {
        setChatHistory(prev => [...prev, { sender: "ai", text: data.answer }])
      } else {
        setChatHistory(prev => [...prev, { sender: "ai", text: "❌ Error generating answer." }])
      }
    } catch (error) {
      setChatHistory(prev => [...prev, { sender: "ai", text: "❌ Connection error. Is your FastAPI server running?" }])
    }
    setIsAsking(false)
  }

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans">
      
      {/* SIDEBAR */}
      <div className="w-80 bg-gray-800 border-r border-gray-700 p-4 flex flex-col">
        <h1 className="text-xl font-bold mb-6 text-blue-400">AI Repo Copilot</h1>
        
        <div className="flex flex-col gap-3">
          <label className="text-sm text-gray-400 font-semibold">Load Repository</label>
          <input
            type="text"
            placeholder="Paste public GitHub URL..."
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            className="p-2 bg-gray-900 border border-gray-700 rounded outline-none focus:border-blue-500 text-sm"
          />
          <button 
            onClick={handleAnalyzeRepo}
            disabled={isAnalyzing}
            className={`bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded transition-colors ${isAnalyzing ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            {isAnalyzing ? "Analyzing..." : "Analyze Repo"}
          </button>
        </div>
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col h-screen">
        
        {/* Chat History Window */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`flex gap-4 ${msg.sender === "human" ? "flex-row-reverse" : ""}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm shrink-0 ${msg.sender === "human" ? "bg-green-500" : "bg-blue-500"}`}>
                {msg.sender === "human" ? "U" : "AI"}
              </div>
              <div className={`p-4 rounded-lg max-w-3xl text-sm leading-relaxed ${msg.sender === "human" ? "bg-green-900/30 rounded-tr-none border border-green-800" : "bg-gray-800 rounded-tl-none border border-gray-700"}`}>
              {msg.sender === "ai" ? (
              <Typewriter text={msg.text} />
              ) : (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              )}
              </div>
            </div>
          ))}
          {/* Loading indicator when asking */}
          {isAsking && (
             <div className="flex gap-4">
               <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center font-bold text-sm shrink-0">AI</div>
               <div className="p-4 rounded-lg bg-gray-800 rounded-tl-none text-sm text-gray-400 italic">Thinking...</div>
             </div>
          )}
        </div>

        {/* Input Box Area */}
        <div className="p-4 bg-gray-800 border-t border-gray-700">
          <div className="max-w-4xl mx-auto flex gap-2">
            <input
              type="text"
              placeholder="Ask a question about the code..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-3 outline-none focus:border-blue-500"
            />
            <button 
              onClick={handleSendMessage}
              disabled={isAsking || !question}
              className={`bg-blue-600 hover:bg-blue-500 px-6 font-semibold rounded-lg transition-colors ${(isAsking || !question) ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              Send
            </button>
          </div>
        </div>

      </div>
    </div>
  )
}

export default App