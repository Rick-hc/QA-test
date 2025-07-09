import React from 'react'
// このコードは、ユーザーが選択肢から質問を選ぶためのコンポーネントです。
interface Props {
  candidates: string[]
  onSelect: (q: string) => void
}

const CandidateList: React.FC<Props> = ({ candidates, onSelect }) => {
  const [other, setOther] = React.useState('')

  return (
    <div className="space-y-2">
      {candidates.map(c => (
        <label key={c} className="block">
          <input type="radio" name="cand" value={c} onChange={() => onSelect(c)} /> {c}
        </label>
      ))}
      <input type="radio" name="cand" value={other} onChange={() => onSelect(other)} />
      <input value={other} onChange={e => setOther(e.target.value)} className="border" placeholder="その他" />
    </div>
  )
}

export default CandidateList
