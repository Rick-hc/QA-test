import React from 'react'

interface Props {
  q2: string
  onLoad: (answer: string, url: string) => void
}

const AnswerView: React.FC<Props> = ({ q2, onLoad }) => {
  const [content, setContent] = React.useState('')
  React.useEffect(() => {
    const run = async () => {
      const resSearch = await fetch('/api/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({candidates: [q2], threshold: 0})
      })
      const hit = (await resSearch.json()).results[0]
      const resAns = await fetch('/api/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({q_id: hit.q_id})
      })
      const data = await resAns.json()
      setContent(data.answer)
      onLoad(data.answer, data.pdf_url)
    }
    run()
  }, [q2])

  return (
    <div className="border p-2 whitespace-pre-wrap">
      {content}
    </div>
  )
}

export default AnswerView
