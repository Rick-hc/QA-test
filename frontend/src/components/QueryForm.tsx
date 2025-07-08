import { useState } from 'react'

export default function QueryForm({ onResult }: { onResult: (c: string[]) => void }) {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const submit = async () => {
    setLoading(true)
    const res = await fetch('/query/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_query:text})})
    const data = await res.json()
    setLoading(false)
    onResult(data.candidates)
  }
  return (
    <div>
      <textarea value={text} onChange={e=>setText(e.target.value)} className="w-full border" />
      <button onClick={submit} disabled={loading}>検索</button>
    </div>
  )
}
