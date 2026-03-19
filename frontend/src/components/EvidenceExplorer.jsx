export default function EvidenceExplorer({ evidence, question }) {
  const evidenceCards =
    evidence && evidence.length
      ? evidence.map((item, index) => ({
          id: item.chunkId || `${item.title}-${index}`,
          title: item.title,
          relevance: item.score,
          signal: item.sources?.length ? item.sources.join(" + ") : "retrieval",
          excerpt: item.excerpt,
        }))
      : [
          {
            id: "empty-evidence",
            title: "Waiting for indexed evidence",
            relevance: 0.0,
            signal: "pending",
            excerpt: `Run a query after uploading documents to see live supporting evidence for: ${question}`,
          },
        ];

  return (
    <section className="module-stage" id="evidence">
      <div className="module-stage-copy">
        <p className="eyebrow">Module 03</p>
        <h2>Evidence Explorer</h2>
        <p>
          This area explains why the system answered the way it did. It turns retrieval
          from a black box into a visible research aid.
        </p>
      </div>

      <div className="evidence-grid">
        {evidenceCards.map((card) => (
          <article className="evidence-source-card" key={card.id}>
            <div className="evidence-source-topline">
              <h3>{card.title}</h3>
              <span>{Math.round(card.relevance * 100)}% match</span>
            </div>
            <p className="evidence-signal">
              Strong overlap with <strong>{card.signal}</strong>
            </p>
            <p>{card.excerpt}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
