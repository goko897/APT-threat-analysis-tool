import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import ResultDisplay from './components/ResultDisplay';
import Navbar from './components/NavBar';
import './App.css';

const App = () => {
  const [result, setResult] = useState(null);
  const [timeSpent, setTimeSpent] = useState(0); // Track time spent in seconds

  // Start a timer when the user loads the page
  useEffect(() => {
    const interval = setInterval(() => {
      setTimeSpent((prevTime) => prevTime + 1);
    }, 1000);

    return () => clearInterval(interval); // Cleanup timer on unmount
  }, []);

  const handleFileSubmit = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    // Call backend API to process the file and get results
    const response = await fetch('http://localhost:3000/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'result.csv';
      link.click();
      window.URL.revokeObjectURL(url);
    } else {
      console.error('Error analyzing file');
      setResult({ error: 'Error analyzing file' });
    }
  };

  // Format the time into minutes and seconds
  const formatTime = (timeInSeconds) => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = timeInSeconds % 60;
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds} minutes`;
  };

  return (
    <div>
      <Navbar timeSpent={formatTime(timeSpent)} />
      <div className="App">
        <h1>APT Analysis Tool</h1>
        <FileUpload onSubmit={handleFileSubmit} />
        {result && <ResultDisplay data={result} />}
      </div>
    </div>
  );
};

export default App;
