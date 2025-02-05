const SetupGuide = {
  id: "setup-guide",
  title: "Setup Guide",
  subtopics: [
    {
      id: "installation",
      title: "Installation",
      content: `
# 🔧 Installation

## 1️⃣ Install Dependencies
Run:

\`\`\`bash
npm install
\`\`\`

## 2️⃣ Start Development Server
\`\`\`bash
npm run dev
\`\`\`
      `,
    },
    {
      id: "configuration",
      title: "Configuration",
      content: `
# ⚙️ Configuration

Modify \`config.js\` as follows:

\`\`\`javascript
const config = {
  apiKey: "YOUR_API_KEY",
  mode: "development",
};
export default config;
\`\`\`
      `,
    },
  ],
};

export default SetupGuide;