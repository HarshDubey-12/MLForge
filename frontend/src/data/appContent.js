export const moduleRoadmap = [
  {
    id: "query",
    name: "Research Query Workspace",
    status: "Live prototype",
    description: "Ask a question, inspect the answer, and check confidence before acting.",
  },
  {
    id: "intake",
    name: "Document Intake",
    status: "Live prototype",
    description: "Upload PDFs and watch them move into the retrieval system.",
  },
  {
    id: "evidence",
    name: "Evidence Explorer",
    status: "Live evidence",
    description: "Surface retrieved evidence cards and explain why the system answered the way it did.",
  },
  {
    id: "conversation",
    name: "Conversation Memory",
    status: "Live prototype",
    description: "Extend single-turn research into a guided multi-turn workspace.",
  },
];

export const ingestionStages = [
  { name: "Parse", detail: "Extract text and structure from uploaded PDFs." },
  { name: "Clean", detail: "Normalize document noise and preserve useful metadata." },
  { name: "Chunk", detail: "Split long papers into retrieval-friendly sections." },
  { name: "Embed", detail: "Generate vectors for semantic matching." },
  { name: "Index", detail: "Store chunks and metadata for downstream retrieval." },
];

export const initialQuestion =
  "Summarize the latest trends in retrieval-augmented generation for scientific literature review systems.";

export const initialQueryResult = {
  answer:
    "The strongest systems combine hybrid retrieval, adaptive query planning, and answer verification rather than relying on a single embedding lookup.",
  confidence: 0.84,
  planSummary:
    "Hybrid retrieval selected top 3 contexts to answer the current question.",
  needsRevision: false,
  evidence: [
    {
      chunkId: "seed-1",
      title: "Adaptive RAG for Scientific Workflows.pdf",
      excerpt:
        "Hybrid retrieval improves recall in terminology-heavy literature, especially when dense and lexical signals are blended.",
      score: 0.93,
      sources: ["semantic", "keyword"],
    },
    {
      chunkId: "seed-2",
      title: "Evaluation Strategies for LLM Agents.pdf",
      excerpt:
        "Self-evaluation and answer verification help catch weak grounding before final response generation.",
      score: 0.85,
      sources: ["semantic"],
    },
  ],
};

export const sampleDocuments = [
  {
    id: 1,
    title: "Adaptive RAG for Scientific Workflows.pdf",
    meta: "12.4 MB - PDF - uploaded 5 min ago",
    status: "Indexed",
  },
  {
    id: 2,
    title: "Evaluation Strategies for LLM Agents.pdf",
    meta: "8.1 MB - PDF - uploaded 21 min ago",
    status: "Chunking",
  },
  {
    id: 3,
    title: "Multimodal Retrieval Survey.pdf",
    meta: "15.8 MB - PDF - uploaded 1 hr ago",
    status: "Ready for review",
  },
];

export const initialConversation = [
  {
    id: 1,
    role: "assistant",
    content:
      "I can help you explore papers, compare methods, and build a research brief from your uploaded knowledge base.",
  },
];
