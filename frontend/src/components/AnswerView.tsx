import React from 'react'

interface Props {
  q_id: string
  onLoad: (answer: string, url: string) => void
}

const AnswerView: React.FC<Props> = ({ q_id, onLoad }) => {
  const [content, setContent] = React.useState('')
  React.useEffect(() => {
    const run = async () => {
      const resAns = await fetch('/api/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({q_id})
      })
      const data = await resAns.json()
      setContent(data.answer)
      onLoad(data.answer, data.pdf_url)
    }
    run()
  }, [q_id])

  return (
    <div className="border p-2 whitespace-pre-wrap">
      {content}
    </div>
  )
}

export default AnswerView
