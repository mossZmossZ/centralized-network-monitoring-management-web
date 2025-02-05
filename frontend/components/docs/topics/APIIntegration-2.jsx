const APIIntegration2 = {
    id: "api-integration-2",
    title: "API Integration-2",
    subtopics: [
      {
        id: "fetching-data",
        title: "Fetching Data",
        content: `
  # 🌐 API Integration
  
  To fetch data from the API, use:
  
  \`\`\`javascript
  fetch("https://api.example.com/data")
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
  \`\`\`
  
  ---
  ### Best Practices
  - Always handle errors properly.
  - Use async/await for better readability.
        `,
      },
    ],
  };
  
  export default APIIntegration2;