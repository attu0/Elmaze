function Message({ msg }) {

  const handleDownload = () => {
    const blob = new Blob(["Dummy PCB file content"], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "pcb_design.txt";
    a.click();

    window.URL.revokeObjectURL(url);
  };

  return (
    <div style={{
      textAlign: msg.sender === "user" ? "right" : "left",
      margin: "10px"
    }}>
      <div className={msg.sender === "user" ? "user" : "glass"}>

        {msg.loading ? (
          <>
            <p className="typing">
              ⚙️ Generating<span>.</span><span>.</span><span>.</span>
            </p>
            <p>🔍 Analyzing components...</p>
            <p>⚡ Routing PCB layers...</p>
            <p>🧠 Optimizing layout...</p>
          </>
        ) : (
          <>
            {msg.sender === "bot" && (
              <img
                src="https://cdn.pixabay.com/photo/2016/11/29/04/17/circuit-board-1867736_1280.jpg"
                className="pcb-img"
                alt="pcb"
              />
            )}

            <p>{msg.text}</p>

            {msg.fileUrl && (
              <button className="btn" onClick={handleDownload}>
                ⬇ Download PCB File
              </button>
            )}
          </>
        )}

      </div>
    </div>
  );
}

export default Message;