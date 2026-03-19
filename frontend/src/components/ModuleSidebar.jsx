export default function ModuleSidebar({ modules }) {
  return (
    <aside className="panel panel-secondary">
      <div className="panel-header">
        <div>
          <p className="section-label">Module map</p>
          <h2>Design order</h2>
        </div>
      </div>

      <div className="roadmap">
        {modules.map((module) => (
          <article className="roadmap-item" key={module.name}>
            <div className="roadmap-topline">
              <h3>{module.name}</h3>
              <span>{module.status}</span>
            </div>
            <p>{module.description}</p>
          </article>
        ))}
      </div>

      <article className="highlights-card">
        <div className="section-label">System summary</div>
        <ul>
          <li>Query module proves answer quality.</li>
          <li>Upload module expands the knowledge base.</li>
          <li>Evidence module explains the retrieval path.</li>
          <li>Conversation module supports longer investigations.</li>
        </ul>
      </article>
    </aside>
  );
}
