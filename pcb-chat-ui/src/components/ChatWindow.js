import Message from "./Message";

function ChatWindow({ messages }) {
  return (
    <div style={{ flex: 1, overflowY: "auto", padding: "20px" }}>
      {messages.length === 0 && (
        <div style={{ textAlign: "center", marginTop: "150px" }}>
          <h2>⚡ Welcome to PCB AI Designer</h2>
          <p>Describe your PCB...</p>
        </div>
      )}

      {messages.map((msg, i) => (
        <Message key={i} msg={msg} />
      ))}
    </div>
  );
}

export default ChatWindow;