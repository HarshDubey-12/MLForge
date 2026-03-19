import { useEffect, useMemo, useState } from "react";

import ConversationPanel from "./components/ConversationPanel";
import DocumentIntakeSection from "./components/DocumentIntakeSection";
import EvidenceExplorer from "./components/EvidenceExplorer";
import HeroBanner from "./components/HeroBanner";
import ModuleSidebar from "./components/ModuleSidebar";
import QueryWorkspace from "./components/QueryWorkspace";
import { API_BASE_URL } from "./config/api";
import {
  ingestionStages,
  initialConversation,
  initialQueryResult,
  initialQuestion,
  moduleRoadmap,
  sampleDocuments,
} from "./data/appContent";

export default function App() {
  const [question, setQuestion] = useState(initialQuestion);
  const [queryResult, setQueryResult] = useState(initialQueryResult);
  const [queryStatus, setQueryStatus] = useState("Ready");
  const [isQuerying, setIsQuerying] = useState(false);
  const [documents, setDocuments] = useState(sampleDocuments);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadState, setUploadState] = useState("No file selected");
  const [isUploading, setIsUploading] = useState(false);
  const [messages, setMessages] = useState(initialConversation);
  const [conversationDraft, setConversationDraft] = useState("");
  const [isSending, setIsSending] = useState(false);

  const libraryStats = useMemo(() => {
    const indexed = documents.filter((document) =>
      ["Indexed", "Ready for review"].includes(document.status),
    ).length;
    const processing = documents.length - indexed;

    return {
      total: documents.length,
      processing,
      ready: indexed,
    };
  }, [documents]);

  useEffect(() => {
    setQueryStatus("Connected to query-first workspace");
  }, []);

  async function handleQuerySubmit(event) {
    event.preventDefault();

    if (!question.trim()) {
      setQueryStatus("Enter a question before running the query.");
      return;
    }

    setIsQuerying(true);
    setQueryStatus("Running adaptive query...");

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`Query request failed with status ${response.status}`);
      }

      const data = await response.json();
      setQueryResult({
        answer: data.answer || "No answer returned.",
        confidence: Number.isFinite(data.confidence) ? data.confidence : 0.5,
        planSummary: data.plan_summary || "The backend did not return a plan summary.",
        needsRevision: Boolean(data.needs_revision),
        evidence: Array.isArray(data.evidence)
          ? data.evidence.map((item) => ({
              chunkId: item.chunk_id || null,
              title: item.title || "Untitled source",
              excerpt: item.excerpt || "",
              score: Number.isFinite(item.score) ? item.score : 0,
              sources: Array.isArray(item.sources) ? item.sources : [],
            }))
          : [],
      });
      setQueryStatus("Query completed using the backend route.");
    } catch (error) {
      setQueryResult({
        answer:
          "Backend query is not reachable right now, so this preview is showing a fallback summary of the intended experience.",
        confidence: 0.52,
        planSummary: "Fallback mode is active because the backend query route is unavailable.",
        needsRevision: true,
        evidence: [],
      });
      setQueryStatus(error.message);
    } finally {
      setIsQuerying(false);
    }
  }

  async function handleUploadSubmit(event) {
    event.preventDefault();

    if (!selectedFile) {
      setUploadState("Choose a PDF before uploading.");
      return;
    }

    setIsUploading(true);
    setUploadState("Uploading document...");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE_URL}/upload_documents`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload request failed with status ${response.status}`);
      }

      const data = await response.json();
      setDocuments((currentDocuments) => [
        {
          id: Date.now(),
          title: data.metadata?.title || data.filename || selectedFile.name,
          meta: `${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB - ${selectedFile.type || "file"} - ${data.chunk_count || 0} chunks indexed`,
          status: data.ingestion_status === "processed" ? "Indexed" : "Accepted",
        },
        ...currentDocuments,
      ]);
      setUploadState(`Document accepted by the backend. ${data.chunk_count || 0} chunks processed.`);
      setSelectedFile(null);
    } catch (error) {
      setDocuments((currentDocuments) => [
        {
          id: Date.now(),
          title: selectedFile.name,
          meta: `${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB - local preview only`,
          status: "Queued locally",
        },
        ...currentDocuments,
      ]);
      setUploadState(`${error.message}. Added local placeholder instead.`);
      setSelectedFile(null);
    } finally {
      setIsUploading(false);
    }
  }

  async function handleConversationSubmit(event) {
    event.preventDefault();

    if (!conversationDraft.trim()) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: conversationDraft,
    };

    setMessages((currentMessages) => [...currentMessages, userMessage]);
    setConversationDraft("");
    setIsSending(true);

    try {
      const response = await fetch(`${API_BASE_URL}/conversation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          role: "user",
          content: userMessage.content,
        }),
      });

      if (!response.ok) {
        throw new Error(`Conversation request failed with status ${response.status}`);
      }

      const data = await response.json();
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now() + 1,
          role: "assistant",
          content:
            data.reply ||
            "The backend conversation route responded without a message body.",
          evidence: Array.isArray(data.evidence)
            ? data.evidence.map((item) => ({
                chunkId: item.chunk_id || null,
                title: item.title || "Untitled source",
              }))
            : [],
        },
      ]);
    } catch (error) {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: Date.now() + 1,
          role: "assistant",
          content:
            "The live conversation service is not reachable, so this is a local fallback response that preserves the workflow.",
          evidence: [],
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace-frame">
        <HeroBanner modules={moduleRoadmap} />

        <div className="workspace-grid">
          <QueryWorkspace
            isQuerying={isQuerying}
            onQuestionChange={setQuestion}
            onSubmit={handleQuerySubmit}
            queryResult={queryResult}
            queryStatus={queryStatus}
            question={question}
          />
          <ModuleSidebar modules={moduleRoadmap} />
        </div>

        <DocumentIntakeSection
          documents={documents}
          ingestionStages={ingestionStages}
          isUploading={isUploading}
          libraryStats={libraryStats}
          onFileChange={setSelectedFile}
          onSubmit={handleUploadSubmit}
          selectedFile={selectedFile}
          uploadState={uploadState}
        />

        <EvidenceExplorer
          evidence={queryResult.evidence}
          question={question}
        />

        <ConversationPanel
          draft={conversationDraft}
          isSending={isSending}
          messages={messages}
          onDraftChange={setConversationDraft}
          onSend={handleConversationSubmit}
        />
      </section>
    </main>
  );
}
