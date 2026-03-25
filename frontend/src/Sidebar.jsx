import "./Sidebar.css";
import { useContext } from "react";
import { MyContext } from "./MyContext.jsx";

function Sidebar() {
  const { setNewChat, setPrompt, setReply, setPrevChats } = useContext(MyContext);

  const createNewChat = () => {
    setNewChat(true);
    setPrompt("");
    setReply(null);
    setPrevChats([]);
  };

  return (
    <section className="sidebar">
      <button onClick={createNewChat}>
        {/* <img src="/assets/blacklogo.png" alt="logo" className="logo" /> */}
        <span><i className="fa-solid fa-pen-to-square"></i></span>
      </button>

      <div className="history">
        <p style={{ padding: "10px" }}>PCB Generator</p>
      </div>

      <div className="sign">
        <p>PCB Generator UI</p>
      </div>
    </section>
  );
}

export default Sidebar;