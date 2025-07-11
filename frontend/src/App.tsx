import React from 'react'
import QueryForm from './components/QueryForm'
import CandidateList from './components/CandidateList'
import AnswerView from './components/AnswerView'
import FeedbackButtons from './components/FeedbackButtons'

const App: React.FC = () => {
  interface SearchResult {
    q_id: string
    question: string
    score: number
  }

  const [results, setResults] = React.useState<SearchResult[]>([])
  const [selected, setSelected] = React.useState<string>('')
  const [answer, setAnswer] = React.useState<string>('')
  const [pdfUrl, setPdfUrl] = React.useState<string>('')

  const runSearch = async (candidates: string[]) => {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidates, threshold: 0, topk: 5 })
    })
    const data = await res.json()
    setResults(data.results)
  }

    return (
      <div className="p-4 space-y-4">
        <QueryForm onResult={runSearch} />
        {results.length > 0 && (
          <CandidateList results={results} onSelect={setSelected} />
        )}
        {selected && (
          <AnswerView q_id={selected} onLoad={(a, url) => { setAnswer(a); setPdfUrl(url) }} />
        )}
        {answer && <FeedbackButtons query={selected} />}
      </div>
    )
  }

export default App
