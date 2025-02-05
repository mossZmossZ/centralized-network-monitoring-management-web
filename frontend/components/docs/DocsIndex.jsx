import { useState, useEffect } from "react";
import Sidebar from "./sidebar";
import Content from "./Content";
import Introduction from "./topics/Introduction";
import SetupGuide from "./topics/SetupGuide";
import APIIntegration from "./topics/APIIntegration";
import APIIntegration2 from "./topics/APIIntegration-2";


const topics = [Introduction, SetupGuide, APIIntegration, APIIntegration2];

export default function DocsIndex() {
  // ✅ Immediately set the first available topic
  const [activeTopic, setActiveTopic] = useState(topics[0]?.subtopics[0] || null);

  // ✅ Ensure `activeTopic` is updated if topics exist but state is null
  useEffect(() => {
    if (!activeTopic && topics.length > 0) {
      setActiveTopic(topics[0].subtopics[0]); // ✅ Prevents empty state
    }
  }, [topics]);
  console.log("Loaded topics:", topics);
  console.log("Active Topic:", activeTopic);
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar topics={topics} activeTopic={activeTopic} setActiveTopic={setActiveTopic} />
      {activeTopic ? (
        <Content activeTopic={activeTopic} />
      ) : (
        <p className="p-8 text-gray-600">Select a topic from the sidebar.</p>
      )}
    </div>
  );
}