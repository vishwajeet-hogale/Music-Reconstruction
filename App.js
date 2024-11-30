import React, { useState } from "react";
import Header from "./Components/Header";
import "./App.css";

function App() {
  const [stage, setStage] = useState(0); // Tracks the current stage
  const [loading, setLoading] = useState(false); // Tracks if the loading screen is active
  const [uploadedFiles, setUploadedFiles] = useState([]); // Tracks uploaded MIDI files

  // Handles the recycling process
  const handleRecycleClick = () => {
    setLoading(true); // Show the loading screen
    setTimeout(() => {
      setLoading(false); // Hide the loading screen
      setStage((prevStage) => prevStage + 1); // Move to the next stage
    }, 5000); // Simulate 5 seconds delay
  };

  // Handles MIDI file uploads
  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files); // Convert FileList to an array
    const midiFiles = files.filter((file) => file.type === "audio/midi");

    if (midiFiles.length > 0) {
      setUploadedFiles(midiFiles);
      alert(
        `Uploaded ${midiFiles.length} MIDI file(s): ${midiFiles
          .map((file) => file.name)
          .join(", ")}`
      );
    } else {
      alert("Please upload valid MIDI files only!");
    }
  };

  // Handles navigating back to the previous stage
  const handleBackClick = () => {
    if (stage > 0) {
      setStage(stage - 1);
    }
  };

  return (
    <div className="App">
      <Header />

      {/* Back Button */}
      {stage > 0 && (
        <button className="back-button" onClick={handleBackClick}>
          Back
        </button>
      )}

      {/* MIDI File Upload Section */}
      {stage === 0 && (
        <>
          <h1>Upload MIDI Files</h1>
          <input
            type="file"
            accept=".midi,.mid"
            className="upload-button"
            onChange={handleFileUpload}
            multiple // Allows selecting multiple files
          />
          {uploadedFiles.length > 0 && (
            <div>
              <h2>Uploaded Files:</h2>
              <ul>
                {uploadedFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
          <h1>Recycle Music</h1>
          <button className="recycle-button" onClick={handleRecycleClick}>
            ♻
          </button>
        </>
      )}

      {/* Recycling Section */}
      {loading ? (
        <h1>Recycling...</h1>
      ) : (
        stage > 0 && (
          <>
            {stage <= 4 && (
              <div>
                <h2>After {stage * 100} generations</h2>
                <div id="audio">
                <audio controls src="song.mp3" type="audio/mp3" />
              </div>
                <button className="recycle-button" onClick={handleRecycleClick}>
                  Continue Recycling ♻
                </button>
              </div>
            )}
            {stage === 5 && (
              <div>
                <h2>Fully Recycled Audio</h2>
                <audio controls>
                  <source src="final-audio.mp3" type="audio/mp3" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </>
        )
      )}
    </div>
  );
}

export default App;
