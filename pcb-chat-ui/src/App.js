import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [started, setStarted] = useState(false);
  const [history, setHistory] = useState([]);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ✅ SEND MESSAGE
  const sendMessage = (text) => {
    if (!text.trim()) return;

    setStarted(true);

    const userMsg = { text, sender: "user" };
    const loadingMsg = { text: "Thinking...", sender: "bot", loading: true };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);

    // simulate AI response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          text: "✅ PCB Generated Successfully\n⚡ Optimized routing & layout",
          sender: "bot",
          file: true,
        },
      ]);
    }, 1500);

    setInput("");
  };

  // ✅ ENTER KEY SUPPORT
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  // ✅ NEW CHAT
  const newChat = () => {
    if (messages.length > 0) {
      setHistory((prev) => [...prev, messages]);
    }
    setMessages([]);
    setStarted(false);
  };

  // ✅ LOAD HISTORY
  const loadHistory = (chat) => {
    setMessages(chat);
    setStarted(true);
  };

  // ✅ DELETE HISTORY
  const deleteHistory = (index) => {
    setHistory((prev) => prev.filter((_, i) => i !== index));
  };

  // ✅ DOWNLOAD FILE
  const downloadFile = () => {
    const blob = new Blob(["PCB DATA"], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pcb_design.txt";
    a.click();
  };

  return (
    <div className="app">

      {/* 🔥 SIDEBAR */}
      <div className="sidebar">
        <button className="newChatBtn" onClick={newChat}>
          + New Chat
        </button>

        <div className="history">
          <h4>History</h4>
          {history.map((chat, index) => (
            <div key={index} className="historyItem">
              <span onClick={() => loadHistory(chat)}>
                Chat {index + 1}
              </span>
              <button onClick={() => deleteHistory(index)}>🗑</button>
            </div>
          ))}
        </div>
      </div>

      {/* 💬 MAIN */}
      <div className="main">

        {/* HEADER */}
        <h2 className="header">⚡ PCB AI Designer</h2>

        {/* CHAT AREA */}
        <div className={`chat ${started ? "active" : "center"}`}>
          {messages.map((msg, i) => (
            <div key={i} className={`msg ${msg.sender}`}>
              <div className="bubble">
                {msg.loading ? (
                  <span className="typing">...</span>
                ) : (
                  <>
                    <p>{msg.text}</p>
                    {msg.file && (
                      <button
                        className="downloadBtn"
                        onClick={downloadFile}
                      >
                        ⬇ Download PCB File
                      </button>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* INPUT */}
        <div className={`inputArea ${started ? "bottom" : "center"}`}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your PCB..."
          />
          <button onClick={() => sendMessage(input)}>Send</button>
        </div>

      </div>
    </div>
  );
}

export default App;