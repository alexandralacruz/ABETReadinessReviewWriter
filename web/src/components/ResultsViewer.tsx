import React, { useState } from 'react'

export default function ResultsViewer({ results }: { results: any[] }) {
  const [selected, setSelected] = useState<number | null>(null)
  const [approved, setApproved] = useState<Record<number, boolean>>({})

  return (
    <div className="results">
      <h2>Evaluation Results</h2>
      <ul>
        {results.map((r, idx) => (
          <li key={idx} className="result-item">
            <div className="summary">
              <strong>{r.criterion_id || r.criterionId || `Criterion ${idx + 1}`}</strong>
              <span>Score: {String(r.score)}</span>
              <span>Confidence: {typeof r.confidence === 'number' ? r.confidence.toFixed(2) : r.confidence}</span>
              <button onClick={() => setSelected(selected === idx ? null : idx)}>{selected === idx ? 'Hide' : 'Details'}</button>
              <label>
                <input type="checkbox" checked={!!approved[idx]} onChange={(e) => setApproved({ ...approved, [idx]: e.target.checked })} /> Approve
              </label>
            </div>
            {selected === idx && (
              <div className="details">
                <h4>Justification</h4>
                <pre>{r.justification}</pre>
                <h4>Evidence refs</h4>
                <ul>
                  {(r.evidence_refs || r.evidenceRefs || []).map((er: any, i: number) => (
                    <li key={i}><strong>{er.source}</strong> (page {er.page}) — <code>{er.excerpt}</code></li>
                  ))}
                </ul>
                <h4>Recommended actions</h4>
                <ul>
                  {(r.recommended_actions || r.recommendedActions || []).map((a: any, i: number) => <li key={i}>{a}</li>)}
                </ul>
                <h4>Raw JSON</h4>
                <pre>{JSON.stringify(r, null, 2)}</pre>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
