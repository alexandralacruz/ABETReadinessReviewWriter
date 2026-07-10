import React, { useState } from 'react'
import axios from 'axios'
import ResultsViewer from './components/ResultsViewer'

export default function App() {
  const [files, setFiles] = useState<FileList | null>(null)
  const [results, setResults] = useState<any[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!files || files.length === 0) return
    setLoading(true)
    setError(null)
    const form = new FormData()
    Array.from(files).forEach((f) => form.append('files', f))
    try {
      const resp = await axios.post('/api/evaluate', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      setResults(resp.data)
    } catch (err: any) {
      setError(err?.response?.data || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>ABET Readiness Reviewer</h1>
      <form onSubmit={handleUpload}>
        <input type="file" multiple onChange={(e) => setFiles(e.target.files)} />
        <button type="submit" disabled={loading}>Run Evaluation</button>
      </form>
      {loading && <p>Running evaluation — this may take a minute (calls LLM provider).</p>}
      {error && <pre className="error">{JSON.stringify(error, null, 2)}</pre>}
      {results && <ResultsViewer results={results} />}
    </div>
  )
}
