import React, { useState, useEffect } from "react";
import Header from "./Header";
import "./App.css";

function App() {
  const [stage, setStage] = useState(0); // Tracks the current stage
  const [loading, setLoading] = useState(false); // Tracks if the loading screen is active
  const [uploadedFiles, setUploadedFiles] = useState([]); // Tracks uploaded MIDI files
  const [songs, setSongs] = useState([]);
  const [genComplete, setGenComplete] = useState(-1); // Tracks the list of song filenames

  // Fetch the list of songs from the backend when the component mounts
  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/songs");
        if (response.ok) {
          const data = await response.json();
          setSongs(data.songs); // Assuming backend returns { songs: ['section_1.wav', 'section_2.wav', ...] }
        } else {
          console.error("Failed to fetch songs");
        }
      } catch (error) {
        console.error("Error fetching songs:", error);
      }
    };

    fetchSongs();
  }, []);

  // Handles the recycling process
  const handleRecycleClick = async () => {
    if (genComplete === 1){
    setLoading(true); // Show the loading screen
    setTimeout(() => {
      setLoading(false); // Hide the loading screen
      setStage((prevStage) => prevStage + 1); // Move to the next stage
    }, 1000);
   }
   else{
    alert("Genetic Algorithm still running!!!")
   }
    // Simulate 5 seconds delay
  };

  // Handles MIDI file uploads
  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files); // Convert FileList to an array
    const midiFiles = files.filter((file) => file.type === "audio/midi");
    setGenComplete(0)
    if (midiFiles.length > 0) {
      setUploadedFiles(midiFiles);
      alert(
        `Uploaded ${midiFiles.length} MIDI file(s): ${midiFiles
          .map((file) => file.name)
          .join(", ")}`
      );

      // Prepare the FormData object to send files to the backend
      const formData = new FormData();
      midiFiles.forEach((file, index) => {
        formData.append(`file_${index}`, file); // Append each file
      });

      try {
        // Send the files to the backend using a POST request
        const uploadResponse = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (uploadResponse.ok) {
          alert("Files uploaded successfully!");
        } else {
          alert("Failed to upload files. Please try again.");
        }
      } catch (error) {
        alert("An error occurred while uploading files.");
        console.error("Error during file upload:", error);
      }

      // Trigger the backend run operation
      try {
        const runResponse = await fetch("http://127.0.0.1:5000/run", {
          method: "GET",
        });

        if (runResponse.ok) {
          const result = await runResponse.json();
          if (result["result"] === 1) {
            setGenComplete(1); // Set generation complete
          }
        } else {
          alert("Failed to process the files.");
        }
      } catch (error) {
        alert("An error occurred while processing the files.");
        console.error("Error during processing:", error);
      }
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
          {
            // add loading animation here something that spins.
            genComplete === 0 ? (
            <>
             <div className="spinner"></div>
            </>
            ) :
          
           (
            <>
              <h1>Recycle Music</h1>
              <button className="recycle-button" onClick={handleRecycleClick}>
                ♻ Recycle
              </button>
            </>
          )}
        </>
      )}

      {/* Recycling Section */}
      {loading ? (
        <h1>Recycling...</h1>
      ) : (
        stage > 0 &&
        stage <= songs.length && (
          <>
            <h2>Stage {stage}: {songs[stage - 1]}</h2>
            <div id="audio">
              <button
                className="download-button"
                onClick={() =>
                  window.open(
                    `http://127.0.0.1:5000/songs/${songs[stage - 1]}`,
                    "_blank"
                  )
                }
              >
                Download
              </button>
              <audio controls>
                <source
                  src={`http://127.0.0.1:5000/songs/${songs[stage - 1]}`}
                  type="audio/wav"
                />
                Your browser does not support the audio element.
              </audio>
            </div>
            <button className="recycle-button" onClick={handleRecycleClick}>
              Next Stage ♻
            </button>
          </>
        )
      )}

      {/* If all stages are completed */}
      {stage > songs.length && (
        <div>
          <h2>Fully Recycled Audio</h2>
          <audio controls>
            <source src="http://127.0.0.1:5000/songs/section_1.wav" type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
}

export default App;
