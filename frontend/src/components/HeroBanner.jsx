export default function HeroBanner({ modules }) {
  return (
    <header className="hero-banner">
      <div className="hero-copy">
        <p className="eyebrow">MLForge Research Workspace</p>
        <h1>Complete the research workflow, not just the landing page.</h1>
        <p className="lede">
          This frontend now covers the main product modules: ask, ingest, inspect,
          and continue the investigation. The design is built to teach the system
          while also making it usable.
        </p>
      </div>

      <nav className="hero-nav" aria-label="Module navigation">
        {modules.map((module) => (
          <a className="hero-link" href={`#${module.id}`} key={module.id}>
            <strong>{module.name}</strong>
            <span>{module.status}</span>
          </a>
        ))}
      </nav>
    </header>
  );
}
