import { useState } from 'react'
import QueryForm from './components/QueryForm'
import CandidateList from './components/CandidateList'
import AnswerView from './components/AnswerView'
import FeedbackButtons from './components/FeedbackButtons'

function App() {
  const [candidates, setCandidates] = useState<string[]>([])
  const [answer, setAnswer] = useState<{text:string,url?:string}>()
  const [selected, setSelected] = useState<string|undefined>()

  return (
    <div className="p-4">
      <QueryForm onResult={setCandidates} />
      {candidates.length > 0 && (
        <CandidateList candidates={candidates} onSelect={(c) => {
          setSelected(c)
          fetch('/search/', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({candidates:[c],threshold:0.7})})
            .then(res=>res.json())
            .then(data=>{
              if(data.hits.length){
                fetch('/answer/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q_id:data.hits[0].q_id})})
                .then(res=>res.json()).then(a=>setAnswer({text:a.answer,url:a.pdf_url}))
              }
            })
        }} />
      )}
      {answer && <AnswerView answer={answer.text} pdfUrl={answer.url} />}
      {selected && <FeedbackButtons selected={selected} />}
    </div>
  )
}

export default App
