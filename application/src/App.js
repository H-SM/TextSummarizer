import "./App.css";
import React, { useState } from "react";
import logo from "./assets/logo.png";
function App() {
  const [summary, setSummary] = useState("");
  const [articleLen, setArticleLen] = useState(0);
  const [summLen, setSummLen] = useState(0);
  const [showBox, setShowBox] = useState(0);
  const [percentage, setPercentage] = useState(0);
  const [url, setUrl] = useState("");

  const handleUrlChange = (event) => {
    const newValue = event.target.value;
    setUrl(newValue);
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    const endpointUrl = "http://localhost:5000/summary";
    setShowBox(1);
    setSummary("Loading...");
    setArticleLen(0);
    setSummLen(0);
    fetchSummary(endpointUrl);
  };
  const fetchSummary = async (endpointUrl) => {
    try {
      const response = await fetch(endpointUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          percentage: percentage,
        }),
      });
      const data = await response.json();
      setSummary(data.summary);
      setArticleLen(data.lengthA);
      setSummLen(data.lengthS);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };
  const handlePercentageChange = (event) => {
    const newValue = parseInt(event.target.value);
    setPercentage(newValue);
  };

  const handleCopy = () => {
    const textarea = document.getElementById("summaryTextarea");
    textarea.select();
    document.execCommand("copy");
  };
  return (
    <div className="text-[2rem] mx-[5rem] mt-[10rem] font-Nothing font-medium h-full">
      <div className="w-fit h-fit flex gap-2">
        TEXT SUMMARIZER @ HSM
        <img src={logo} alt="logo" className="w-[3rem] h-[3rem]"/>
      </div>
      <form onSubmit={handleSubmit} class="mt-8 font-SourceCodePro">
        <div class="relative z-0 w-full mb-5 group">
          <input
            type="text"
            name="floating_URL"
            id="floating_URL"
            class="block py-2.5 px-0 w-[49vw] text-sm bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 peer"
            placeholder=" "
            required
            onChange={handleUrlChange}
            pattern="https?://.+"
          />
          <label
            for="floating_URL"
            class="peer-focus:font-medium absolute text-sm  duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
          >
            URL
          </label>
        </div>
        <div class="relative z-0 w-[4em] mb-5 group">
          <input
            type="number"
            name="floating_Precentage"
            id="floating_Precentage"
            class="block py-2.5 px-0 w-full text-sm bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 peer"
            placeholder=" "
            required
            min="0"
            max="100"
            onChange={handlePercentageChange}
          />
          <label
            for="floating_Precentage"
            class="peer-focus:font-medium font-sans absolute text-sm duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
          >
            Percentage
          </label>
        </div>
        <button
          type="submit"
          className="border border-1 border-black border-opacity-55 font-Nothing font-semibold px-5 py-3 bg-transparentw-[8rem] h-[3rem] rounded-lg text-[1rem] flex justify-center items-center scale-95 hover:scale-100 transition ease-in-out duration-200"
        >
          SUBMIT
        </button>
      </form>
      {showBox === 1 && (
        <div>
          <h3 className="text-[2rem] mt-10">OUTPUT</h3>
          <div className="text-[0.9rem] font-SourceCodePro mt-2 flex flex-col">
            {articleLen !== 0 && (
              <>
                <p>Article → Summary</p>
                <p>
                  {articleLen} → {summLen}
                </p>
              </>
            )}
            <div className="flex gap-2">
              <button
                onClick={handleCopy}
                className="border border-1 border-black border-opacity-55 font-Nothing font-semibold px-5 bg-transparent w-[8rem] h-[3rem] rounded-lg text-[1rem] flex justify-center items-center scale-95 hover:scale-100 transition ease-in-out duration-200"
              >
                Copy
              </button>

              <button
                onClick={() => {
                  setSummary("");
                  setArticleLen(0);
                  setSummLen(0);
                }}
                className="border border-1 border-black border-opacity-55 font-Nothing font-semibold px-5 bg-transparent w-[8rem] h-[3rem] rounded-lg text-[1rem] flex justify-center items-center scale-95 hover:scale-100 transition ease-in-out duration-200"
              >
                Clear
              </button>
            </div>
            <textarea
              id="summaryTextarea"
              cols="30"
              rows="35"
              className="border border-black/30 rounded-md outline-none px-1 py-1 w-[80vw] h-full mt-2 bg-transparent"
              value={summary}
              readOnly
            ></textarea>
          </div>
        </div>
      )}
      <footer className="w-full  h-[5rem] mt-20 flex justify-center items-end pb-3 text-[1rem]">
        Made by @ HSM
      </footer>
    </div>
  );
}

export default App;
