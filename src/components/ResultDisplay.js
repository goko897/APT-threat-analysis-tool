import React from 'react';

const ResultDisplay = ({ data }) => {
  return (
    <div>
      <h2>APT Analysis Result</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default ResultDisplay;

