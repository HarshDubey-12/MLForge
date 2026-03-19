export default function DocumentIntakeSection({
  documents,
  ingestionStages,
  isUploading,
  libraryStats,
  onFileChange,
  onSubmit,
  selectedFile,
  uploadState,
}) {
  return (
    <section className="module-stage" id="intake">
      <div className="module-stage-copy">
        <p className="eyebrow">Module 02</p>
        <h2>Document Intake</h2>
        <p>
          Uploaded papers are the raw material of the research assistant. This
          module makes the ingestion pipeline visible so the system feels teachable,
          not opaque.
        </p>
      </div>

      <div className="intake-grid">
        <section className="panel panel-primary">
          <div className="panel-header">
            <div>
              <p className="section-label">Upload workspace</p>
              <h3>Add research documents</h3>
            </div>
            <span className="status-pill status-pill-soft">{uploadState}</span>
          </div>

          <form onSubmit={onSubmit}>
            <label className="dropzone-card" htmlFor="document-upload">
              <div className="dropzone-icon">+</div>
              <h3>Drop PDFs here or click to browse</h3>
              <p>
                Upload papers, surveys, or notes to prepare them for parsing,
                chunking, embedding, and indexing.
              </p>
              <input
                id="document-upload"
                className="file-input"
                type="file"
                accept=".pdf,.txt,.md"
                onChange={(event) => onFileChange(event.target.files?.[0] || null)}
              />
              <span className="file-name">
                {selectedFile ? selectedFile.name : "No file selected yet"}
              </span>
            </label>

            <div className="action-row">
              <button type="submit" disabled={isUploading}>
                {isUploading ? "Uploading..." : "Upload document"}
              </button>
              <p>
                The frontend uses `POST /upload_documents` when reachable and creates
                a local placeholder item if the API is offline.
              </p>
            </div>
          </form>

          <div className="pipeline-card">
            <div className="section-label">Ingestion pipeline</div>
            <div className="pipeline-flow">
              {ingestionStages.map((stage) => (
                <article className="pipeline-step" key={stage.name}>
                  <strong>{stage.name}</strong>
                  <p>{stage.detail}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="panel panel-secondary">
          <div className="panel-header">
            <div>
              <p className="section-label">Library status</p>
              <h3>Recently uploaded documents</h3>
            </div>
          </div>

          <div className="document-list">
            {documents.map((document) => (
              <article className="document-item" key={document.id}>
                <div className="document-copy">
                  <h3>{document.title}</h3>
                  <p>{document.meta}</p>
                </div>
                <span className="document-status">{document.status}</span>
              </article>
            ))}
          </div>

          <div className="stats-grid">
            <article className="stat-card">
              <span>Total papers</span>
              <strong>{String(libraryStats.total).padStart(2, "0")}</strong>
            </article>
            <article className="stat-card">
              <span>Currently processing</span>
              <strong>{String(libraryStats.processing).padStart(2, "0")}</strong>
            </article>
            <article className="stat-card">
              <span>Ready for retrieval</span>
              <strong>{String(libraryStats.ready).padStart(2, "0")}</strong>
            </article>
          </div>
        </section>
      </div>
    </section>
  );
}
