export default function ConversationPanel({
  draft,
  isSending,
  messages,
  onDraftChange,
  onSend,
}) {
  return (
    <section className="module-stage" id="conversation">
      <div className="module-stage-copy">
        <p className="eyebrow">Module 04</p>
        <h2>Conversation Memory</h2>
        <p>
          Once the single-query workflow works, researchers need a place to refine,
          compare, and continue the investigation over multiple turns.
        </p>
      </div>

      <div className="conversation-shell panel panel-primary">
        <div className="panel-header">
          <div>
            <p className="section-label">Session workspace</p>
            <h3>Multi-turn research thread</h3>
          </div>
          <span className="status-pill status-pill-soft">
            {isSending ? "Sending..." : "Ready"}
          </span>
        </div>

        <div className="conversation-list">
          {messages.map((message) => (
            <article
              className={`message-card message-card-${message.role}`}
              key={message.id}
            >
              <span className="message-role">{message.role}</span>
              <p>{message.content}</p>
            </article>
          ))}
        </div>

        <form className="conversation-form" onSubmit={onSend}>
          <label className="composer" htmlFor="conversation-input">
            <span className="composer-label">Continue the discussion</span>
            <textarea
              id="conversation-input"
              value={draft}
              onChange={(event) => onDraftChange(event.target.value)}
              rows={4}
              placeholder="Ask a follow-up question, compare two papers, or request a summary."
            />
          </label>
          <div className="action-row">
            <button type="submit" disabled={isSending}>
              {isSending ? "Sending..." : "Send turn"}
            </button>
            <p>
              This uses the backend conversation route when available and falls back to a
              local placeholder response if it fails.
            </p>
          </div>
        </form>
      </div>
    </section>
  );
}
