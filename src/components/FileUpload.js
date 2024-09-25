import React, { useState } from 'react';

const FileUpload = ({ onSubmit }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      await onSubmit(file);
    } else {
      alert('Please select a file first.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="file-upload">Upload Network Analysis File:</label>
      <input
        id="file-upload"
        type="file"
        accept=".txt,.csv,.json,.gml,.gexf"
        onChange={handleFileChange}
      />
      <button type="submit">Analyze</button>
    </form>
  );
};

export default FileUpload;
