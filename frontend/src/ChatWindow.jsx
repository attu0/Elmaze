import "./ChatWindow.css";
import { useState } from "react";
import { ScaleLoader } from "react-spinners";

function ChatWindow() {
  const [width, setWidth] = useState("");
  const [height, setHeight] = useState("");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  // 🆕 store file
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [fileName, setFileName] = useState("");

  // =========================
  // WIDTH + HEIGHT
  // =========================
  const generatePCB = async () => {
    if (!width || !height) {
      alert("Please enter width and height");
      return;
    }

    setLoading(true);
    setDownloadUrl(null); // reset old file

    try {
      const response = await fetch("http://localhost:8000/api/generate-pcb", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          width: parseFloat(width),
          height: parseFloat(height)
        })
      });

      if (!response.ok) {
        const err = await response.json();
        alert(err.error || "Error generating PCB");
        setLoading(false);
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      setDownloadUrl(url);
      setFileName("pcb_gerber.zip");

    } catch (err) {
      console.log(err);
      alert("Error generating PCB");
    }

    setLoading(false);
  };

  // =========================
  // PROMPT → FILE
  // =========================
  const generateFromPrompt = async () => {
    if (!prompt) {
      alert("Enter a prompt");
      return;
    }

    setLoading(true);
    setDownloadUrl(null); // reset old file

    try {
      const response = await fetch("http://localhost:8000/api/generate-from-prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) {
        const err = await response.json();
        alert(err.error || "Error from backend");
        setLoading(false);
        return;
      }

      const blob = await response.blob();

      if (blob.size === 0) {
        alert("Empty file received");
        setLoading(false);
        return;
      }

      const url = window.URL.createObjectURL(blob);

      setDownloadUrl(url);
      setFileName("pcb_from_prompt.zip");

    } catch (err) {
      console.log(err);
      alert("Failed to fetch file");
    }

    setLoading(false);
  };

  return (
    <div className="chatWindow">

      {/* NAVBAR */}
      <div className="navbar">
        <span>PCB Generator ⚡</span>
      </div>

      {/* CENTER */}
      <div style={{
        flex: 1,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: "100%"
      }}>
        <form
          style={{ maxWidth: "600px", width: "100%" }}
          onSubmit={(e) => {
            e.preventDefault();
            generatePCB();
          }}
        >
          <h2 style={{ textAlign: "center" }}>PCB Parameters</h2>

          <input
            placeholder="Width (inches)"
            value={width}
            onChange={(e) => setWidth(e.target.value)}
          />

          <input
            placeholder="Height (inches)"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
          />

          <button type="submit" style={{ marginTop: "1rem" }}>
            Generate PCB
          </button>

          <ScaleLoader color="#fff" loading={loading} />

          {/* 🆕 DOWNLOAD BUTTON */}
          {downloadUrl && (
            <a href={downloadUrl} download={fileName}>
              <button type="button" style={{ marginTop: "1rem" }}>
                ⬇ Download PCB
              </button>
            </a>
          )}
        </form>
      </div>

      {/* CHAT INPUT */}
      <div className="chatInput">
        <form
          className="inputBox"
          onSubmit={(e) => {
            e.preventDefault();
            generateFromPrompt();
          }}
        >
          <input
            placeholder="Describe your PCB..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />

          <button type="submit" id="submit">
            ➤
          </button>
        </form>

        {/* 🆕 DOWNLOAD BUTTON FOR PROMPT */}
        {downloadUrl && (
          <a href={downloadUrl} download={fileName}>
            <button style={{ marginTop: "10px" }}>
              ⬇ Download Result
            </button>
          </a>
        )}
      </div>
    </div>
  );
}

export default ChatWindow;