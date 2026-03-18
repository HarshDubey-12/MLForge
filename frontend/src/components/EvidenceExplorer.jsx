import { useMemo } from "react";

export default function EvidenceExplorer({ question, answer, documents }) {
  const evidenceCards = useMemo(() => {
    const seedTerms = question
      .toLowerCase()
      .split(/[^a-z0-9]+/)
      .filter((term) => term.length > 4)
      .slice(0, 3);

    return documents.slice(0, 3).map((document, index) => ({
      id: `${document.id}-${index}`,
      title: document.title,
      relevance: 0.93 - index * 0.08,
      signal:
        seedTerms[index] ||
        ["retrieval", "evaluation", "knowledge"][index] ||
        "research",
      excerpt:
        answer ||
        "Evidence will appear here once the query and document systems are connected to live backend retrieval traces.",
    }));
  }, [answer, documents, question]);

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
