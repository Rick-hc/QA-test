import React from 'react'
// このコードは、ユーザーが選択肢から質問を選ぶためのコンポーネントです。
interface Candidate {
  q_id: string
  question: string
}

interface Props {
  results: Candidate[]
  onSelect: (q_id: string) => void
}

const CandidateList: React.FC<Props> = ({ results, onSelect }) => {
  return (
    <div className="space-y-2">
      {results.map(r => (
        <label key={r.q_id} className="block">
          <input
            type="radio"
            name="cand"
            value={r.q_id}
            onChange={() => onSelect(r.q_id)}
          /> {r.question}
        </label>
      ))}
    </div>
  )
}

export default CandidateList
