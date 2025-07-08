import React from 'react'

interface Props {
  onResult: (candidates: string[]) => void
}

const QueryForm: React.FC<Props> = ({ onResult }) => {
  const [query, setQuery] = React.useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const res = await fetch('/api/query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_query: query})
    })
    const data = await res.json()
    onResult(data.candidates)
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      <textarea value={query} onChange={e => setQuery(e.target.value)} className="w-full border p-2" />
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white">検索</button>
    </form>
  )
}

export default QueryForm
