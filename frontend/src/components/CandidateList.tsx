export default function CandidateList({ candidates, onSelect }: { candidates: string[]; onSelect: (s: string) => void }) {
  return (
    <div>
      {candidates.map((c, i) => (
        <div key={i}>
          <input type="radio" name="cand" id={c} onChange={()=>onSelect(c)} />
          <label htmlFor={c}>{c}</label>
        </div>
      ))}
      <div>
        <input type="radio" name="cand" id="other" onChange={()=>onSelect('')} />
        <label htmlFor="other">その他</label>
      </div>
    </div>
  )
}
