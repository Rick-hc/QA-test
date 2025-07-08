export default function AnswerView({ answer, pdfUrl }: { answer: string; pdfUrl?: string }) {
  return (
    <div>
      <div dangerouslySetInnerHTML={{__html: answer}} />
      {pdfUrl && <a href={pdfUrl} target="_blank" rel="noreferrer">PDF</a>}
    </div>
  )
}
