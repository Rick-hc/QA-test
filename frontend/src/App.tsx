import React from 'react'
import QueryForm from './components/QueryForm'
import CandidateList from './components/CandidateList'
import AnswerView from './components/AnswerView'
import FeedbackButtons from './components/FeedbackButtons'

const App: React.FC = () => {
  const [candidates, setCandidates] = React.useState<string[]>([])
  const [selected, setSelected] = React.useState<string>('')
  const [answer, setAnswer] = React.useState<string>('')
  const [pdfUrl, setPdfUrl] = React.useState<string>('')

  return (
    <div className="p-4 space-y-4">
      <QueryForm onResult={setCandidates} />
      {candidates.length > 0 && (
        <CandidateList candidates={candidates} onSelect={setSelected} />
      )}
      {selected && (
        <AnswerView q2={selected} onLoad={(a, url) => { setAnswer(a); setPdfUrl(url) }} />
      )}
      {answer && <FeedbackButtons query={selected} />}
    </div>
  )
}

export default App
