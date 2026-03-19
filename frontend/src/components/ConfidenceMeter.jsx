export default function ConfidenceMeter({ value }) {
  const safeValue = Number.isFinite(value) ? value : 0;
  const width = `${Math.max(0, Math.min(100, Math.round(safeValue * 100)))}%`;

  return (
    <div className="confidence-card">
      <div className="section-label">Confidence</div>
      <div className="confidence-row">
        <strong>{Math.round(safeValue * 100)}%</strong>
        <span>Answer reliability estimate</span>
      </div>
      <div className="confidence-track" aria-hidden="true">
        <div className="confidence-fill" style={{ width }} />
      </div>
    </div>
  );
}
