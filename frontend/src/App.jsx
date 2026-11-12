
import { useState } from 'react'
import './App.css'

function App() {
  const [logType, setLogType] = useState('Linux')
  const [logContent, setLogContent] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [analysisHistory, setAnalysisHistory] = useState([])

  const handleAnalyze = async () => {
    if (!logContent.trim()) {
      alert('Please enter log content before analyzing.')
      return
    }

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          logType: logType,
          logContent: logContent,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        alert(data.message || 'Analysis failed.')
        return
      }

      setAnalysisResult(data.analysis)

      const historyEntry = {
        id: Date.now(),
        logType: logType,
        error: data.analysis.error,
        severity: data.analysis.severity || 'Low',
        date: new Date().toLocaleString(),
      }

      setAnalysisHistory((previousHistory) => [
        historyEntry,
        ...previousHistory,
      ])
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Unable to connect to the backend. Please check Flask.')
    }
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2>⚙ DevOps AI</h2>

        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Linux Logs</a>
          <a href="#">Docker Logs</a>
          <a href="#">Jenkins Logs</a>
          <a href="#history">Analysis History</a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="dashboard-header">
          <div>
            <h1>DevOps AI Dashboard</h1>
            <p>Analyze and troubleshoot your DevOps logs</p>
          </div>
          <span className="system-status">● System Online</span>
        </header>

        <section className="stats-grid">
          <div className="stat-card">
            <h3>128</h3>
            <p>Total Logs</p>
          </div>

          <div className="stat-card">
            <h3>24</h3>
            <p>Errors Detected</p>
          </div>

          <div className="stat-card">
            <h3>18</h3>
            <p>Issues Resolved</p>
          </div>

          <div className="stat-card">
            <h3>3</h3>
            <p>Services</p>
          </div>
        </section>

        <section className="analyzer-card">
          <h2>Log Analyzer</h2>
          <p>Select a technology and enter its log content.</p>

          <label htmlFor="logType">Log Type</label>
          <select
            id="logType"
            value={logType}
            onChange={(event) => setLogType(event.target.value)}
          >
            <option value="Linux">Linux</option>
            <option value="Docker">Docker</option>
            <option value="Jenkins">Jenkins</option>
          </select>

          <label htmlFor="logContent">Log Content</label>
          <textarea
            id="logContent"
            rows="7"
            placeholder="Paste your Linux, Docker, or Jenkins logs here..."
            value={logContent}
            onChange={(event) => setLogContent(event.target.value)}
          />

          <button onClick={handleAnalyze}>Analyze Logs</button>

          {analysisResult && (
            <div className="result-card">
              <h3>Analysis Results</h3>

              <p>
                <strong>Detected Error:</strong> {analysisResult.error}
              </p>

              <p>
                <strong>Severity:</strong>{' '}
                <span
                  className={`severity severity-${(
                    analysisResult.severity || 'low'
                  ).toLowerCase()}`}
                >
                  {analysisResult.severity || 'Not Assigned'}
                </span>
              </p>

              <p>
                <strong>Root Cause:</strong> {analysisResult.root_cause}
              </p>

              <p>
                <strong>Recommendation:</strong>{' '}
                {analysisResult.recommendation}
              </p>
            </div>
          )}
        </section>

        <section className="analyzer-card" id="history">
          <h2>Analysis History</h2>
          <p>Review your previous log analysis results.</p>

          {analysisHistory.length === 0 ? (
            <p>No analysis history available yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Technology</th>
                  <th>Detected Error</th>
                  <th>Severity</th>
                  <th>Date &amp; Time</th>
                </tr>
              </thead>

              <tbody>
                {analysisHistory.map((item) => (
                  <tr key={item.id}>
                    <td>{item.logType}</td>
                    <td>{item.error}</td>
                    <td>{item.severity}</td>
                    <td>{item.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
