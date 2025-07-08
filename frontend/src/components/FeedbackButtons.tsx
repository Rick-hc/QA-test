import React from 'react'

interface Props {
  query: string
}

const FeedbackButtons: React.FC<Props> = ({ query }) => {
  const send = async (good: boolean) => {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_query: query, q1_list: [], selected_q2: query, topk: good ? 1 : 0})
    })
  }

  return (
    <div className="space-x-2">
      <button onClick={() => send(true)} className="px-2 py-1 bg-green-500 text-white">👍</button>
      <button onClick={() => send(false)} className="px-2 py-1 bg-red-500 text-white">👎</button>
    </div>
  )
}

export default FeedbackButtons
