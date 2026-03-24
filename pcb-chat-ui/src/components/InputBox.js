import { useState } from "react";

function InputBox({ sendMessage }) {
  const [input, setInput] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
      setInput("");
    }
  };

  return (
    <div style={{ display: "flex", width: "60%" }}>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Describe your PCB..."
        style={{
          flex: 1,
          padding: "12px",
          borderRadius: "12px",
          border: "1px solid #00f5ff",
          background: "#020617",
          color: "white"
        }}
      />

      <button
        onClick={() => {
          sendMessage(input);
          setInput("");
        }}
        className="btn"
        style={{ marginLeft: "10px" }}
      >
        Send
      </button>
    </div>
  );
}

export default InputBox;