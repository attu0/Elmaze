function Sidebar() {
  return (
    <div style={{
      width: "220px",
      background: "rgba(0,0,0,0.5)",
      padding: "10px"
    }}>
      <button className="btn" style={{ width: "100%" }}>
        + New Chat
      </button>

      <p style={{ marginTop: "20px", fontSize: "14px" }}>
        History (Coming Soon)
      </p>
    </div>
  );
}

export default Sidebar;