export const fetchAPTAnalysis = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error fetching analysis:', error);
      return null;
    }
  };
  