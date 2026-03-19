import ConfidenceMeter from "./ConfidenceMeter";

export default function QueryWorkspace({
  isQuerying,
  onSubmit,
  onQuestionChange,
  queryResult,
  queryStatus,
  question,
}) {
  return (
    <section className="panel panel-primary" id="query">
      <div className="panel-header">
        <div>
          <p className="section-label">Module 01</p>
          <h2>Research Query Workspace</h2>
        </div>
        <span className="status-pill">{queryStatus}</span>
      </div>

      <form onSubmit={onSubmit}>
        <label className="composer" htmlFor="research-question">
          <span className="composer-label">Research question</span>
          <textarea
            id="research-question"
            value={question}
            onChange={(event) => onQuestionChange(event.target.value)}
            rows={5}
          />
        </label>

        <div className="action-row">
          <button type="submit" disabled={isQuerying}>
            {isQuerying ? "Running..." : "Run adaptive query"}
          </button>
          <p>
            The frontend calls `POST /query` when available and falls back to a
            local preview if the backend is offline.
          </p>
        </div>
      </form>

      <div className="insight-grid">
        <article className="answer-card">
          <div className="section-label">Answer preview</div>
          <p>{queryResult.answer}</p>
        </article>
        <ConfidenceMeter value={queryResult.confidence} />
      </div>

      <article className="plan-card">
        <div className="section-label">Retrieval plan</div>
        <p>{queryResult.planSummary}</p>
        <span className={`revision-chip ${queryResult.needsRevision ? "revision-chip-warn" : ""}`}>
          {queryResult.needsRevision ? "Needs revision" : "Grounding looks stable"}
        </span>
      </article>

      <article className="evidence-card">
        <div className="section-label">Why this module comes first</div>
        <ul>
          <li>It matches the live `/query` API the backend already exposes.</li>
          <li>It makes trust visible through the answer and confidence pair.</li>
          <li>It anchors every later module in a real user outcome.</li>
        </ul>
      </article>
    </section>
  );
}
